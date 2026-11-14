"""TRELLIS Cryptographic Security: Argon2id, Asymmetric RS256 JWT, JWKS, Key Rotation & Field-Level Encryption."""

import base64
import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import jwt
import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.config import settings

# 1. Argon2id Password Hasher
pwd_hasher = PasswordHasher(
    time_cost=settings.ARGON2_TIME_COST,
    memory_cost=settings.ARGON2_MEMORY_COST,
    parallelism=settings.ARGON2_PARALLELISM,
)


def hash_password(password: str) -> str:
    """Hash plaintext password using Argon2id."""
    return pwd_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify plaintext password against Argon2id hash."""
    try:
        return pwd_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


# 2. Asymmetric RSA Key Manager & Key Rotation Registry
CURRENT_KEY_ID = "trellis-key-2026-v1"

# Store: kid -> (private_key | None, public_key)
_KEY_REGISTRY: dict[str, tuple[rsa.RSAPrivateKey | None, rsa.RSAPublicKey]] = {}
_ACTIVE_KEY_ID: str = CURRENT_KEY_ID


def _init_asymmetric_keys() -> None:
    """Initialize asymmetric RSA keypair from filesystem or ephemeral dev pair."""
    global _ACTIVE_KEY_ID
    priv_path = Path(settings.JWT_PRIVATE_KEY_PATH)
    pub_path = Path(settings.JWT_PUBLIC_KEY_PATH)

    if settings.TRELLIS_ENV != "dev" and (not priv_path.exists() or not pub_path.exists()):
        raise RuntimeError(
            f"FATAL: Production JWT signing keys missing ({settings.JWT_PRIVATE_KEY_PATH}, {settings.JWT_PUBLIC_KEY_PATH}). "
            "Ephemeral development keys are strictly forbidden outside TRELLIS_ENV=dev."
        )

    if priv_path.exists() and pub_path.exists():
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
            assert isinstance(private_key, rsa.RSAPrivateKey)
        with open(pub_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
            assert isinstance(public_key, rsa.RSAPublicKey)
        _KEY_REGISTRY[CURRENT_KEY_ID] = (private_key, public_key)
    else:
        # Generate development RSA keypair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        _KEY_REGISTRY[CURRENT_KEY_ID] = (private_key, public_key)

    _ACTIVE_KEY_ID = CURRENT_KEY_ID


_init_asymmetric_keys()


def register_rotated_key(
    kid: str,
    private_key: rsa.RSAPrivateKey | None,
    public_key: rsa.RSAPublicKey,
    make_active: bool = False,
) -> None:
    """Register a new or previous RSA key into the JWKS registry for key rotation."""
    global _ACTIVE_KEY_ID
    _KEY_REGISTRY[kid] = (private_key, public_key)
    if make_active:
        _ACTIVE_KEY_ID = kid


def get_active_kid() -> str:
    """Return currently active key identifier."""
    return _ACTIVE_KEY_ID


def get_private_pem(kid: str | None = None) -> bytes:
    """Export private key in PEM format for specified kid or active key."""
    target_kid = kid or _ACTIVE_KEY_ID
    entry = _KEY_REGISTRY.get(target_kid)
    if not entry or not entry[0]:
        raise ValueError(f"No private key available for kid '{target_kid}'")
    return entry[0].private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def get_public_pem(kid: str | None = None) -> bytes:
    """Export public key in PEM format for specified kid or active key."""
    target_kid = kid or _ACTIVE_KEY_ID
    entry = _KEY_REGISTRY.get(target_kid)
    if not entry:
        raise ValueError(f"No key found for kid '{target_kid}'")
    return entry[1].public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def create_access_token(
    subject: str,
    org_id: str,
    roles: list[str],
    expires_delta: timedelta | None = None,
    kid: str | None = None,
) -> str:
    """Issue a signed JWT access token using the active (or specified) RSA private key."""
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    signing_kid = kid or _ACTIVE_KEY_ID
    payload = {
        "sub": subject,
        "org_id": org_id,
        "roles": roles,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": "trellis-auth-server",
        "aud": "trellis-api",
    }

    token = jwt.encode(
        payload,
        get_private_pem(signing_kid),
        algorithm="RS256",
        headers={"kid": signing_kid},
    )
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    """Verify and decode a JWT access token resolving public key via header 'kid'."""
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid", _ACTIVE_KEY_ID)
    if kid not in _KEY_REGISTRY:
        raise jwt.InvalidKeyError(f"Token kid '{kid}' is not recognized in active or rotated keys.")

    public_pem = get_public_pem(kid)
    return jwt.decode(
        token,
        public_pem,
        algorithms=["RS256"],
        audience="trellis-api",
        issuer="trellis-auth-server",
    )


def get_jwks() -> dict[str, Any]:
    """Generate RFC 7517 JSON Web Key Set exposing all active and rotated public keys."""

    def int_to_base64url(val: int) -> str:
        length = (val.bit_length() + 7) // 8
        bytes_val = val.to_bytes(length, byteorder="big")
        return base64.urlsafe_b64encode(bytes_val).decode("utf-8").rstrip("=")

    keys = []
    for kid, (_, pub_key) in _KEY_REGISTRY.items():
        public_numbers = pub_key.public_numbers()
        jwk = {
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": kid,
            "n": int_to_base64url(public_numbers.n),
            "e": int_to_base64url(public_numbers.e),
        }
        keys.append(jwk)

    return {"keys": keys}


# 3. Refresh Tokens & Cryptographic Hashing
def generate_secure_token() -> str:
    """Generate high-entropy random token string for refresh tokens and MFA exchange tickets."""
    return secrets.token_urlsafe(48)


def hash_token(raw_token: str) -> str:
    """Compute SHA-256 hash of a raw token for secure database storage."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


# 4. Field-Level Encryption (AES-256 / Fernet)
def _get_fernet() -> Fernet:
    """Derive authenticated Fernet cipher instance from configured field encryption key."""
    key_bytes = hashlib.sha256(settings.FIELD_ENCRYPTION_KEY.encode("utf-8")).digest()
    b64_key = base64.urlsafe_b64encode(key_bytes)
    return Fernet(b64_key)


def encrypt_field(plaintext: str) -> str:
    """Encrypt sensitive attribute at rest using AES-256 authenticated cipher."""
    if not plaintext:
        return ""
    fernet = _get_fernet()
    return fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_field(ciphertext: str) -> str:
    """Decrypt sensitive attribute retrieved from storage."""
    if not ciphertext:
        return ""
    fernet = _get_fernet()
    return fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")


# 5. TOTP MFA (RFC 6238)
def generate_totp_secret() -> str:
    """Generate a random Base32 TOTP secret key."""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str) -> str:
    """Generate standard otpauth:// URI for QR code provisioning in authenticator apps."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name="TRELLIS (CSM Technology)")


def verify_totp(secret: str, code: str) -> bool:
    """Verify a 6-digit TOTP code with standard 30s window and +/- 1 skew."""
    totp = pyotp.TOTP(secret)
    return bool(totp.verify(code, valid_window=1))

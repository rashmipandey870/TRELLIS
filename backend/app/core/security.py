"""TRELLIS Cryptographic Security: Argon2id, Asymmetric RS256 JWT, JWKS & TOTP MFA."""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import jwt
import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
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


# 2. Asymmetric RSA Key Manager & Rotation
CURRENT_KEY_ID = "trellis-key-2026-v1"


# Generate or load active RSA private & public keys
def _init_asymmetric_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Load asymmetric RSA keys from files or generate an ephemeral development pair."""
    priv_path = Path(settings.JWT_PRIVATE_KEY_PATH)
    pub_path = Path(settings.JWT_PUBLIC_KEY_PATH)

    if priv_path.exists() and pub_path.exists():
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
            assert isinstance(private_key, rsa.RSAPrivateKey)
        with open(pub_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
            assert isinstance(public_key, rsa.RSAPublicKey)
        return private_key, public_key

    # Generate development RSA keypair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


_private_key, _public_key = _init_asymmetric_keys()


def get_private_pem() -> bytes:
    """Export active private key in PEM format."""
    return _private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def get_public_pem() -> bytes:
    """Export active public key in PEM format."""
    return _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def create_access_token(
    subject: str,
    org_id: str,
    roles: list[str],
    expires_delta: timedelta | None = None,
) -> str:
    """Issue a signed JWT access token using the active RSA private key."""
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

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
        get_private_pem(),
        algorithm="RS256",
        headers={"kid": CURRENT_KEY_ID},
    )
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    """Verify and decode a JWT access token using the active RSA public key."""
    return jwt.decode(
        token,
        get_public_pem(),
        algorithms=["RS256"],
        audience="trellis-api",
        issuer="trellis-auth-server",
    )


def get_jwks() -> dict[str, Any]:
    """Generate RFC 7517 JSON Web Key Set (JWKS) exposing public keys for verification."""
    public_numbers = _public_key.public_numbers()

    def int_to_base64url(val: int) -> str:
        """Convert integer to base64url encoded string without padding."""
        length = (val.bit_length() + 7) // 8
        bytes_val = val.to_bytes(length, byteorder="big")
        import base64

        return base64.urlsafe_b64encode(bytes_val).decode("utf-8").rstrip("=")

    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": CURRENT_KEY_ID,
        "n": int_to_base64url(public_numbers.n),
        "e": int_to_base64url(public_numbers.e),
    }

    return {"keys": [jwk]}


# 3. Refresh Tokens & Cryptographic Hashing
def generate_secure_token() -> str:
    """Generate high-entropy random token string for refresh tokens and MFA exchange tickets."""
    return secrets.token_urlsafe(48)


def hash_token(raw_token: str) -> str:
    """Compute SHA-256 hash of a raw token for secure database storage."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


# 4. TOTP MFA (RFC 6238)
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

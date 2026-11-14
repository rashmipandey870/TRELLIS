"""Automated tests validating Asymmetric RSA Key Rotation and Production Invariants."""

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.config import Settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_active_kid,
    get_jwks,
    register_rotated_key,
)


def test_asymmetric_key_rotation_multiple_jwks_and_backwards_compatibility() -> None:
    """Verify that multiple keys exist in JWKS, previous keys decode existing tokens, and new keys sign new tokens."""
    # Step 1: Active key is v1; issue token v1
    initial_kid = get_active_kid()
    assert initial_kid == "trellis-key-2026-v1"

    token_v1 = create_access_token(
        subject="usr_test_rot",
        org_id="org_csm",
        roles=["EMPLOYEE"],
    )
    claims_v1 = decode_access_token(token_v1)
    assert claims_v1["sub"] == "usr_test_rot"

    # Step 2: Generate and register new rotated key v2 and make it active
    v2_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    v2_public = v2_private.public_key()
    v2_kid = "trellis-key-2026-v2"

    register_rotated_key(kid=v2_kid, private_key=v2_private, public_key=v2_public, make_active=True)
    assert get_active_kid() == v2_kid

    # Step 3: Verify JWKS exposes BOTH active key v2 and previous key v1
    jwks = get_jwks()
    kids_in_jwks = [k["kid"] for k in jwks["keys"]]
    assert len(kids_in_jwks) >= 2
    assert "trellis-key-2026-v1" in kids_in_jwks
    assert "trellis-key-2026-v2" in kids_in_jwks

    # Step 4: Issue token v2 using new active key
    token_v2 = create_access_token(
        subject="usr_test_rot",
        org_id="org_csm",
        roles=["EMPLOYEE"],
    )
    unverified_header_v2 = jwt.get_unverified_header(token_v2)
    assert unverified_header_v2["kid"] == "trellis-key-2026-v2"

    claims_v2 = decode_access_token(token_v2)
    assert claims_v2["sub"] == "usr_test_rot"

    # Step 5: Verify that token_v1 issued before rotation STILL DECODES successfully (backwards compatibility)
    claims_v1_recheck = decode_access_token(token_v1)
    assert claims_v1_recheck["sub"] == "usr_test_rot"

    # Step 6: Negative test: Token with unrecognized kid is strictly rejected
    token_bogus_kid = jwt.encode(
        {"sub": "attacker", "iss": "trellis-auth-server", "aud": "trellis-api"},
        "dummy-secret",
        algorithm="HS256",
        headers={"kid": "unknown-foreign-key-id"},
    )
    with pytest.raises(jwt.InvalidKeyError) as exc_info:
        decode_access_token(token_bogus_kid)
    assert "not recognized in active or rotated keys" in str(exc_info.value)


def test_production_environment_refuses_startup_without_keys() -> None:
    """Verify that outside TRELLIS_ENV=dev, the application strictly refuses to start if keys/secrets are missing."""
    with pytest.raises(RuntimeError) as exc_info:
        Settings(
            TRELLIS_ENV="production",
            DATABASE_URL="",
            DATABASE_MIGRATION_URL="",
            JWT_PRIVATE_KEY_PATH="non_existent/private.pem",
            JWT_PUBLIC_KEY_PATH="non_existent/public.pem",
        )
    assert "FATAL" in str(exc_info.value)

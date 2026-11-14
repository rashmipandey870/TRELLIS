"""TRELLIS Test Suite: MultiFernet Authenticated Encryption & Key Rotation."""

from app.core.config import settings
from app.core.security import (
    decrypt_field,
    derive_fernet_key,
    encrypt_field,
    register_rotated_field_key,
    rotate_encrypted_field,
)


def test_hkdf_derivation_produces_valid_32byte_urlsafe_key() -> None:
    raw_passphrase = "my_custom_super_secure_secret_passphrase_2026"
    derived = derive_fernet_key(raw_passphrase)
    assert isinstance(derived, bytes)
    assert len(derived) == 44  # 32 bytes base64 encoded = 44 ASCII characters


def test_multifernet_key_rotation_and_backwards_compatibility() -> None:
    original_key = settings.FIELD_ENCRYPTION_KEY
    try:
        key_1 = "trellis_field_key_rotation_generation_1_2026"
        key_2 = "trellis_field_key_rotation_generation_2_2026"

        # 1. Set key 1 active and encrypt sensitive secret
        settings.FIELD_ENCRYPTION_KEY = key_1
        secret_data = "TOTP_SECRET_BASE32_JBSWY3DPEHPK3PXP"
        ciphertext_v1 = encrypt_field(secret_data)

        assert ciphertext_v1 != secret_data
        assert decrypt_field(ciphertext_v1) == secret_data

        # 2. Rotate to key 2
        register_rotated_field_key(key_2)

        # 3. Invariant: Ciphertext encrypted with key 1 can still be decrypted via MultiFernet
        decrypted_with_rotated = decrypt_field(ciphertext_v1)
        assert decrypted_with_rotated == secret_data

        # 4. New encryption uses Key 2
        ciphertext_v2 = encrypt_field(secret_data)
        assert ciphertext_v2 != ciphertext_v1
        assert decrypt_field(ciphertext_v2) == secret_data

        # 5. Invariant: Old ciphertext can be rotated to new active key
        rotated_ciphertext = rotate_encrypted_field(ciphertext_v1)
        assert decrypt_field(rotated_ciphertext) == secret_data

    finally:
        settings.FIELD_ENCRYPTION_KEY = original_key

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ..config import settings

class SecurityVault:
    """
    A secure vault for encrypting and decrypting sensitive data (like API keys).
    Uses Fernet (AES-128 in CBC mode with HMAC SHA256) for strong encryption.
    """

    def __init__(self):
        self.master_key = settings.secret_vault_key.encode()
        # Verify if the key is a valid Fernet key, otherwise derive one
        try:
            self.fernet = Fernet(self.master_key)
        except Exception:
            # If the provided key isn't valid, we derive a stable key from it
            self.fernet = self._derive_key(self.master_key)

    def _derive_key(self, salt: bytes) -> Fernet:
        """Derives a valid Fernet key from the secret vault key."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"guidely-salt-v1", # Stable salt for derivation
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(salt))
        return Fernet(key)

    def encrypt_api_key(self, plain_text: str, user_id: str) -> str:
        """
        Encrypts an API key bound to a specific user ID.
        Binding to user_id prevents ciphertext from being used by another user.
        """
        if not plain_text:
            return ""
        
        # We prepend the user_id to the plain text to bind the encryption
        bound_text = f"{user_id}:{plain_text}".encode()
        encrypted_bytes = self.fernet.encrypt(bound_text)
        return encrypted_bytes.decode()

    def decrypt_api_key(self, encrypted_text: str, user_id: str) -> str:
        """
        Decrypts an API key and verifies it belongs to the specified user.
        """
        if not encrypted_text:
            return ""
            
        try:
            decrypted_bytes = self.fernet.decrypt(encrypted_text.encode())
            decrypted_text = decrypted_bytes.decode()
            
            # Verify binding
            prefix = f"{user_id}:"
            if not decrypted_text.startswith(prefix):
                raise ValueError("Decryption successful but user ID binding mismatch.")
                
            return decrypted_text[len(prefix):]
        except Exception as e:
            # In production, log this as a potential security event
            raise ValueError(f"Failed to decrypt API key: {str(e)}")

# Global instance
vault = SecurityVault()

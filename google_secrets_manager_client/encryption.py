import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from google_secrets_manager_client.secrets_manager import access_secret_version

salt = b"LOM4h0lOzLG1MDnL"
iv = b"iV2Jw7WufiFdxoUx"
SECRET_ID = "encryption_key"


def get_encryption_key():
    return access_secret_version(secret_id=SECRET_ID)


class CryptoService:

    def __init__(self):
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        key = os.environ[SECRET_ID]
        self.key = kdf.derive(key.encode())

    def encrypt(self, data: str):
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.CTR(iv),
        ).encryptor()
        encrypted_text = encryptor.update(data.encode()) + encryptor.finalize()

        return encrypted_text

    def decrypt(self, encrypted_text: str):
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.CTR(iv),
        ).decryptor()

        return decryptor.update(encrypted_text) + decryptor.finalize()

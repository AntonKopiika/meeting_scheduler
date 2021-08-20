from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from google_secrets_manager_client.secrets_manager import access_secret_version

from meeting_scheduler.app_config import Settings

SECRET_ID = "encryption_key"


def get_encryption_key():
    return access_secret_version(secret_id=SECRET_ID)


class CryptoService:

    def __init__(self):
        key = Settings().encryption_key
        digest = hashes.Hash(hashes.SHA256())
        digest.update(key.encode())
        self.key = digest.finalize()

    def encrypt(self, data: str):
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.ECB(),
        ).encryptor()
        block_size = 16
        pad = " "
        padded_data = data + (block_size - len(data) % block_size) * pad
        encrypted_text = encryptor.update(padded_data.encode()) + encryptor.finalize()

        return encrypted_text

    def decrypt(self, encrypted_text: str):
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.ECB(),
        ).decryptor()
        data = (decryptor.update(encrypted_text) + decryptor.finalize()).strip()

        return data.decode()

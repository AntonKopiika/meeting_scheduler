from google_secrets_manager_client.encryption import CryptoService

from meeting_scheduler.src.models import User, UserAccount


def create_user_account(
        email: str,
        cred: str,
        user: User,
        provider: str,
        description: str = None
):
    crypto_service = CryptoService()
    return UserAccount(
        email=email,
        cred=crypto_service.encrypt(cred),
        user=user,
        user_id=user.id,
        provider=provider,
        description=description
    )


def decrypt_user_cred(user_account: UserAccount):
    crypto_service = CryptoService()
    return crypto_service.decrypt(user_account.cred)

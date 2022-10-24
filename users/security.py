"""Security functions"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: bytes):
    """Password verifivcation

    Args:
        plain_password (str): password from request
        hashed_password (bytes): password hash from db
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Hash password

    Args:
        password (str): plain string"""

    return pwd_context.hash(password)

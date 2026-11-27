"""User account operations, separate from the word guessing game."""

import hashlib
import hmac
import secrets
from typing import Optional, Tuple

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

_PASSWORD_ITERATIONS = 600_000


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PASSWORD_ITERATIONS
    ).hex()


def verify_password(password: str, salt_hex: str, password_hash: str) -> bool:
    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    return hmac.compare_digest(_hash_password(password, salt), password_hash)


def register_user(
    users: Collection, username: str, email: str, password: str
) -> Tuple[bool, str]:
    username = username.strip()
    email = email.strip().lower()
    if not username or not email or not password:
        return False, "Username, email, and password are required."
    local, separator, domain = email.partition("@")
    if (
        not separator
        or not local
        or not domain
        or any(char.isspace() for char in email)
    ):
        return False, "Enter a valid email address."

    existing_user = users.find_one(
        {"$or": [{"username": username}, {"email": email}]}, {"_id": 1}
    )
    if existing_user:
        return False, "Username or email is already registered."

    salt = secrets.token_bytes(16)
    try:
        users.insert_one(
            {
                "username": username,
                "email": email,
                "password_salt": salt.hex(),
                "password_hash": _hash_password(password, salt),
            }
        )
    except DuplicateKeyError:
        return False, "Username or email is already registered."
    return True, "Account created successfully."


def authenticate_user(
    users: Collection, username: str, password: str
) -> Optional[str]:
    if not username.strip() or not password:
        return None

    user = users.find_one(
        {"username": username.strip()},
        {"username": 1, "password_salt": 1, "password_hash": 1},
    )
    if user and verify_password(
        password, user["password_salt"], user["password_hash"]
    ):
        return user["username"]
    return None

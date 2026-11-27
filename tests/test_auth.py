from pymongo.errors import DuplicateKeyError

from auth import authenticate_user, register_user


class _Users:
    def __init__(self):
        self.documents = []

    def find_one(self, query, _projection=None):
        if "$or" in query:
            for document in self.documents:
                if any(
                    document.get(key) == value
                    for clause in query["$or"]
                    for key, value in clause.items()
                ):
                    match = document
                    break
            else:
                match = None
        else:
            match = next(
                (
                    document
                    for document in self.documents
                    if document.get("username") == query.get("username")
                ),
                None,
            )
        if match is None or _projection is None:
            return match
        return {
            key: match[key]
            for key, include in _projection.items()
            if include and key in match
        }

    def insert_one(self, document):
        if any(
            existing["username"] == document["username"]
            or existing["email"] == document["email"]
            for existing in self.documents
        ):
            raise DuplicateKeyError("duplicate account")
        document["_id"] = len(self.documents) + 1
        self.documents.append(document)


def test_registration_stores_password_hash_and_authenticates_user():
    users = _Users()

    success, message = register_user(
        users, "player", "PLAYER@example.com", "secret password"
    )

    assert success
    assert message == "Account created successfully."
    assert users.documents[0]["email"] == "player@example.com"
    assert "password" not in users.documents[0]
    assert users.documents[0]["password_hash"] != "secret password"
    assert authenticate_user(users, "player", "secret password") == "player"


def test_registration_rejects_duplicate_username_or_email():
    users = _Users()
    register_user(users, "player", "player@example.com", "secret")

    success, message = register_user(
        users, "other", "PLAYER@example.com", "another secret"
    )

    assert not success
    assert message == "Username or email is already registered."
    assert len(users.documents) == 1


def test_login_rejects_wrong_password_and_unknown_username():
    users = _Users()
    register_user(users, "player", "player@example.com", "secret")

    assert authenticate_user(users, "player", "wrong") is None
    assert authenticate_user(users, "missing", "secret") is None


def test_registration_rejects_missing_fields():
    success, message = register_user(_Users(), " ", "player@example.com", "secret")

    assert not success
    assert message == "Username, email, and password are required."


def test_registration_rejects_invalid_email():
    success, message = register_user(_Users(), "player", "not-an-email", "secret")

    assert not success
    assert message == "Enter a valid email address."

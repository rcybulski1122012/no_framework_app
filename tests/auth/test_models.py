from app.auth.models import AppUser


def test_user_hashes_password_if_string_given():
    instance = AppUser(
        username="username", password="secret_password_123", email="test@test.com"
    )

    assert isinstance(instance.password, bytes)

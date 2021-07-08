import pytest

from app.auth.models import AppUser
from app.core.errors import ValidationError


def test_user_hashes_password_if_string_given():
    instance = AppUser(
        username="username", password="Secret_password_123", email="test@test.com"
    )

    assert isinstance(instance.password, bytes)


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "username": "wrong",
            "password": "SecretPassword123!",
            "email": "testemail123@wp.pl",
        },
        {
            "username": "too-long-usernemeeeeeeeeeeeeeeeeeeeeee",
            "password": "SecretPassword123!",
            "email": "testemail123@wp.pl",
        },
        {
            "username": "wrong",
            "password": "SecretPassword123!",
            "email": "testemail123@wp.pl",
        },
        {
            "username": "😁😁😁😁😁😁😁😁😁😁",
            "password": "SecretPassword123!",
            "email": "testemail123@wp.pl",
        },
        {
            "username": "proper-username123",
            "password": "SecretPassword123!",
            "email": "invalid-email",
        },
        {
            "username": "proper-username123",
            "password": "SecretPassword123!",
            "email": "*" * 257,
        },
        {
            "username": "proper-username123",
            "password": "invalid-password",
            "email": "*" * 257,
        },
    ],
)
def test_validation(kwargs):
    with pytest.raises(ValidationError):
        AppUser(**kwargs)

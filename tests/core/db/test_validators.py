import pytest

from app.core.db.validators import (
    AllowedCharsValidator,
    EmailValidator,
    MaxLenValidator,
    MinLenValidator,
    PasswordValidator,
)
from app.core.errors import ValidationError


def test_MinLenValidator():
    validator = MinLenValidator(10)

    with pytest.raises(ValidationError):
        validator.validate("abc")

    validator.validate("a" * 10)
    validator.validate("a" * 20)


def test_MaxLenValidator():
    validator = MaxLenValidator(10)

    with pytest.raises(ValidationError):
        validator.validate("a" * 11)

    validator.validate("a")
    validator.validate("a" * 10)


def test_AllowedCharsValidator():
    validator = AllowedCharsValidator()

    with pytest.raises(ValidationError):
        validator.validate("white space are not allowed by default 😁😁😁😜")

    validator.validate("proper-value123")
    validator.validate("|/?!?")


@pytest.mark.parametrize(
    "email",
    [
        "not-valid",
        "not-valid@",
        "@gmail.com",
        "not-valid@gmail",
        "not-valid@.com",
        "e" * 250 + "@gmail.com",
        " ",
    ],
)
def test_EmailValidator(email):
    validator = EmailValidator()

    with pytest.raises(ValidationError):
        validator.validate(email)


@pytest.mark.parametrize(
    "password",
    [
        "pass",
        "a" * 129,
        "lackofbigletters1!",
        "LACK_OF_SMALL_LETTERS2",
        "Lack of special character3",
        "Lack_of_number",
    ],
)
def test_PasswordValidator_invalid_password(password):
    validator = PasswordValidator()

    with pytest.raises(ValidationError):
        validator.validate(password)


def test_PasswordValidator_does_nothing_when_value_is_not_str():
    validator = PasswordValidator()

    validator.validate(b"that-should-be-hashed-password")

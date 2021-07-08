import re
from string import ascii_letters, digits, punctuation

from app.core.errors import ValidationError


class MinLenValidator:
    def __init__(self, length):
        self.length = length

    def validate(self, value, field_name=""):
        if len(value) < self.length:
            raise ValidationError(f"Minimal length of {field_name} is {self.length}.")


class MaxLenValidator:
    def __init__(self, length):
        self.length = length

    def validate(self, value, field_name=""):
        if len(value) > self.length:
            raise ValidationError(f"Maximal length of {field_name} is {self.length}.")


class AllowedCharsValidator:
    def __init__(self, allowed=ascii_letters + digits + punctuation):
        self.allowed = allowed

    def validate(self, value, field_name=""):
        for char in value:
            if char not in self.allowed:
                raise ValidationError(
                    f"You can use only big and small letters, digits and punctuation in {field_name}."
                )


class EmailValidator:
    @staticmethod
    def validate(value, field_name=""):
        MaxLenValidator(256).validate(value, field_name)
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.match(regex, value):
            raise ValidationError("Provide valid email address.")


class PasswordValidator:
    @classmethod
    def validate(cls, value, field_name=""):
        if isinstance(value, str):
            MinLenValidator(8).validate(value, field_name)
            MaxLenValidator(128).validate(value, field_name)
            cls._at_least_one_big_letter(value, field_name)
            cls._at_least_one_small_letter(value, field_name)
            cls._at_least_one_special_character(value, field_name)
            cls._at_least_one_number(value, field_name)

    @staticmethod
    def _at_least_one_big_letter(value, field_name):
        pattern = re.compile(r"[A-Z]")
        if re.search(pattern, value) is None:
            raise ValidationError(f"{field_name} must contain at least one big letter.")

    @staticmethod
    def _at_least_one_small_letter(value, field_name):
        pattern = re.compile(r"[a-z]")
        if re.search(pattern, value) is None:
            raise ValidationError(
                f"{field_name} must contain at least one small letter."
            )

    @staticmethod
    def _at_least_one_special_character(value, field_name):
        pattern = re.compile(f"[{punctuation}]")
        if re.search(pattern, value) is None:
            raise ValidationError(
                f"{field_name} must contain at least one special character. ({punctuation})"
            )

    @staticmethod
    def _at_least_one_number(value, field_name):
        pattern = re.compile(r"[0-9]")
        if re.search(pattern, value) is None:
            raise ValidationError(f"{field_name} must contain at least one digit.")

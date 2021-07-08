import re
from string import ascii_letters, digits, punctuation

from app.core.errors import ValidationError


class MinLenValidator:
    def __init__(self, length):
        self.length = length

    def validate(self, value):
        if len(value) < self.length:
            raise ValidationError(f"Minimal length of this field is {self.length}.")


class MaxLenValidator:
    def __init__(self, length):
        self.length = length

    def validate(self, value):
        if len(value) > self.length:
            raise ValidationError(f"Maximal length of this field is {self.length}.")


class AllowedCharsValidator:
    def __init__(self, allowed=ascii_letters + digits + punctuation):
        self.allowed = allowed

    def validate(self, value):
        for char in value:
            if char not in self.allowed:
                raise ValidationError(
                    "You can use only big and small letters, digits and punctuation."
                )


class EmailValidator:
    @staticmethod
    def validate(value):
        MaxLenValidator(256).validate(value)
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.match(regex, value):
            raise ValidationError("Provide valid email address.")


class PasswordValidator:
    @classmethod
    def validate(cls, value):
        if isinstance(value, str):
            MinLenValidator(8).validate(value)
            MaxLenValidator(128).validate(value)
            cls._at_least_one_big_letter(value)
            cls._at_least_one_small_letter(value)
            cls._at_least_one_special_character(value)
            cls._at_least_one_number(value)

    @staticmethod
    def _at_least_one_big_letter(value):
        pattern = re.compile(r"[A-Z]")
        if re.search(pattern, value) is None:
            raise ValidationError("Password must contain at least one big letter.")

    @staticmethod
    def _at_least_one_small_letter(value):
        pattern = re.compile(r"[a-z]")
        if re.search(pattern, value) is None:
            raise ValidationError("Password must contain at least one small letter.")

    @staticmethod
    def _at_least_one_special_character(value):
        pattern = re.compile(f"[{punctuation}]")
        if re.search(pattern, value) is None:
            raise ValidationError(
                f"Password must contain at least one special character. ({punctuation})"
            )

    @staticmethod
    def _at_least_one_number(value):
        pattern = re.compile(r"[0-9]")
        if re.search(pattern, value) is None:
            raise ValidationError("Password must contain at least one digit.")

from app.core.shortcuts import json_response


class AuthenticationError(Exception):
    pass


class UserDoesNotExist(AuthenticationError):
    @staticmethod
    def get_response(request):
        return json_response(
            request, {"error": "User with this username does not exist."}
        )


class InvalidPasswordError(AuthenticationError):
    @staticmethod
    def get_response(request):
        return json_response(request, {"error": "Invalid password."})


class PasswordsDoNotMatch(AuthenticationError):
    @staticmethod
    def get_response(request):
        return json_response(request, {"error": "Both passwords should be the same."})


class TakenUsernameError(AuthenticationError):
    @staticmethod
    def get_response(request):
        return json_response(request, {"error": "This username is taken."})


class TakenEmailError(AuthenticationError):
    @staticmethod
    def get_response(request):
        return json_response(
            request, {"error": "An account with this email already exists."}
        )

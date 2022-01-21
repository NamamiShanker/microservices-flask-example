"""Global errors are defined here so as the """
from flask import jsonify


class BaseError(Exception):
    """It is a base exception class"""

    def __init__(self, message, status, payload=None):
        self.status = status
        self.message = message
        self.payload = payload


class BadRequest(BaseError):
    """For any bad request , the above class will be called and will render the specific response"""

    pass


def bad_request_handler(error):
    """Catch resource not found error, serialize into JSON, and respond with 404."""
    payload = dict(error.payload or ())
    payload["status"] = error.status
    payload["message"] = error.message
    return jsonify(payload), error.status


class ServerError(BaseError):
    """For any Server Error, the above class will called and will render customized message"""

    pass


def server_error_handler(error):
    """Catch server error and dump to the end user with status 500"""
    payload = dict(error.payload or ())
    payload["status"] = error.status
    payload["message"] = error.message
    return jsonify(payload), error.status

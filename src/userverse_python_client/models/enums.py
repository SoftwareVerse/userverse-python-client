# app/utils/enums/errors.py
from enum import Enum

class Errors(Enum):
    INVALID_REQUEST = "invalid_request"
    INVALID_REQUEST_MESSAGE = "The request was invalid. Please check your input and try again."
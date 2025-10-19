from fastapi import status, HTTPException
from fastapi.requests import Request
import inspect
import traceback
from typing import Optional
import logging


class AppError(HTTPException):
    def __init__(
        self,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: Optional[str] = "Request failed, please try again.",
        error: Optional[str] = None,
        log_error: bool = True,
        depth: int = 3,
    ):
        # Capture where this was raised
        caller = self._get_caller_details(depth)

        # Build the detail dict that will be JSON‐serialized
        error_detail = {
            "message": message,
            "error": error or f"Unexpected error at {caller['file']}:{caller['line']}",
            "location": caller,
        }

        # Log right away
        if log_error:
            logging.error(
                "AppError raised: %r | Error: %r | Location: %s",
                message,
                error_detail["error"],
                caller,
            )

        # Initialize the HTTPException
        super().__init__(status_code=status_code, detail=error_detail)

    @staticmethod
    def _get_caller_details(depth: int):
        frame = inspect.currentframe()
        # walk back `depth` frames
        for _ in range(depth):
            if frame and frame.f_back:
                frame = frame.f_back
        if not frame:
            return {"file": "", "line": 0, "function": ""}
        return {
            "file": frame.f_code.co_filename,
            "line": frame.f_lineno,
            "function": frame.f_code.co_name,
        }

    def log_exception(self):
        """Call this inside an exception handler to log full traceback."""
        tb = traceback.format_exc()
        logging.error("StackTrace:\n %s", tb)
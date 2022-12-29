from .abs_except import AbsException
from typing import Optional


class BadSourceException(AbsException):
    def __init__(self, source_name: str, message: Optional[str] = None, *args, **kwargs):
        super().__init__(message)
        self.source_name = source_name


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        return f"Unable to Load the source by the name \"{self.source_name}\" using any of its available import methods."

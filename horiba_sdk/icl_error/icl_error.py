from typing import final

from loguru import logger
from overrides import override

from horiba_sdk.icl_error.abstract_error import AbstractError, Severity


@final
class ICLError(AbstractError):
    """Represents an Error from the ICL. It has an error code, a message and severity."""

    def __init__(self, code: int, message: str, severity: Severity) -> None:
        self._code = code
        self._message = message
        self._severity = severity

    @override
    def log(self) -> None:
        """Logs the error with the appropriate severity"""
        logger.log(self._severity.name, self._message)

    @override
    def message(self) -> str:
        """Message of error.

        Returns:
            str: message
        """
        return self._message

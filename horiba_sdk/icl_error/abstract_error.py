from abc import ABC, abstractmethod
from enum import Enum
from typing import final

from overrides import override


class AbstractError(ABC):
    """Represents an abstract error."""

    @abstractmethod
    def log(self) -> None:
        """Logs the error."""
        pass

    @abstractmethod
    def message(self) -> str:
        """Returns the message of the error."""
        pass


@final
class FakeError(AbstractError):
    """Fake error"""

    def __init__(self, message: str) -> None:
        self._error_message = message

    @override
    def log(self) -> None:
        """Logs nowhere"""
        pass

    @override
    def message(self) -> str:
        """Returns the message of the error."""
        return self._error_message


class Severity(Enum):
    TRACE = 'TRACE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class StringAsSeverity:
    """StringAsSeverity."""

    def __init__(self, string: str) -> None:
        self._string = string

    def to_severity(self) -> Severity:
        """to_severity.

        Args:

        Returns:
            Severity:
        """
        mapping_dict = {'fatal': Severity.CRITICAL}
        return mapping_dict.get(self._string.lower(), Severity.INFO)

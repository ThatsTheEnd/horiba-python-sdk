from abc import ABC, abstractmethod
from typing import final

from overrides import override

from horiba_sdk.icl_error import AbstractError, FakeError


class AbstractErrorDB(ABC):
    """Abstract error database."""

    @abstractmethod
    def error_from(self, string: str) -> AbstractError:
        """Searches an error in the database based on a string.

        When successfull, returns a corresponding error.
        """
        pass


@final
class FakeErrorDB(AbstractErrorDB):
    @override
    def error_from(self, string: str) -> AbstractError:
        return FakeError(string)

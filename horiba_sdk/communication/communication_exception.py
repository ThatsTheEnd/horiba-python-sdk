from typing import Optional, final


@final
class CommunicationException(Exception):
    """CommunicationException is raised for issues encountered in the communicator classes.

    Specifically all subclasses of horiba_sdk.communication.AbstractCommunicator
    """

    def __init__(self, exception: Optional[Exception] = None, message: str = ''):
        """__init__.

        Args:
            exception (Exception): the lower-level exception
            message (str): explanation of what went wrong
        """
        self.exception = exception
        self.message = message

from enum import Enum
from typing import final


@final
class TimerResolution(Enum):
    """
    .. note:: The timer resolution value of 1 microsecond is not supported by all CCDs.
    """

    _1000_MICROSECONDS = 0
    _1_MICROSECOND = 1

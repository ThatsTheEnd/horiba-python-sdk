from enum import Enum
from typing import final


@final
class XAxisConversionType(Enum):
    """
    Enumeration of possible XAxisConversionTypes
    """

    NONE = 0
    FROM_CCD_FIRMWARE = 1
    FROM_ICL_SETTINGS_INI = 2

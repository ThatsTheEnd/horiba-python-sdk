from enum import Enum
from typing import final


@final
class AcquisitionFormat(Enum):
    SPECTRA = 0
    IMAGE = 1
    CROP = 2
    FAST_KINETICS = 3

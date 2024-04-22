from enum import Enum
from typing import final


@final
class Gain:
    class SyncerityOE(Enum):
        HIGH_SENSITIVITY = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_LIGHT = 2

    class SyncerityNIR(Enum):
        HIGH_SENSITIVITY = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_LIGHT = 2

    class SyncerityUVVis(Enum):
        HIGH_SENSITIVITY = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_LIGHT = 2

    class Synapse2CCD(Enum):
        HIGH_SENSITIVITY = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_LIGHT = 2

    class Symphony2CCD(Enum):
        HIGH_SENSITIVITY = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_LIGHT = 2

    class Synapse2IGA(Enum):
        HIGH_SENSITIVITY = 0
        HIGH_DYNAMIC = 1

    class Symphony2IGA(Enum):
        HIGH_SENSITIVITY = 0
        HIGH_DYNAMIC = 1

    class SynapsePlus(Enum):
        ULTIMATE_SENSITIVITY = 0
        HIGH_SENSITIVITY = 1
        BEST_DYNAMIC_RANGE = 2
        HIGH_LIGHT = 3

    class SynapseEM(Enum):
        ULTIMATE_SENSITIVITY = 0
        HIGH_SENSITIVITY = 1
        BEST_DYNAMIC_RANGE = 2
        HIGH_LIGHT = 3

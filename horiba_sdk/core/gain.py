from enum import Enum
from typing import Union, final


@final
class Gain:
    class SyncerityOE(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2

    class SyncerityNIR(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2

    class SyncerityUVVis(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2

    class Synapse2CCD(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2

    class Symphony2CCD(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2

    class Synapse2IGA(Enum):
        HIGH_DYNAMIC = 0
        HIGH_SENSITIVITY = 1

    class Symphony2IGA(Enum):
        HIGH_DYNAMIC = 0
        HIGH_SENSITIVITY = 1

    class SynapsePlus(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2
        ULTIMATE_SENSITIVITY = 3

    class SynapseEM(Enum):
        HIGH_LIGHT = 0
        BEST_DYNAMIC_RANGE = 1
        HIGH_SENSITIVITY = 2
        ULTIMATE_SENSITIVITY = 3


GainType = Union[
    type[Gain.SyncerityOE],
    type[Gain.SyncerityNIR],
    type[Gain.SyncerityUVVis],
    type[Gain.Synapse2CCD],
    type[Gain.Symphony2CCD],
    type[Gain.Synapse2IGA],
    type[Gain.Symphony2IGA],
    type[Gain.SynapsePlus],
    type[Gain.SynapseEM],
]

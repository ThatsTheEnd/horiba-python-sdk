from enum import Enum
from typing import Union, final


@final
class Speed:
    class SyncerityOE(Enum):
        _45_KHZ = 0
        _1_MHZ = 1
        _1_MHZ_ULTRA = 2

    class SyncerityNIR(Enum):
        _45_KHZ = 0
        _500_KHZ = 1
        _500_KHZ_ULTRA = 2

    class SyncerityUVVis(Enum):
        _45_KHZ = 0
        _500_KHZ = 1
        _500_KHZ_ULTRA = 2

    class Synapse2CCD(Enum):
        _20_KHZ = 0
        _1_MHZ = 1
        _1_MHZ_ULTRA = 2

    class Symphony2CCD(Enum):
        _20_KHZ = 0
        _1_MHZ = 1
        _1_MHZ_ULTRA = 2

    class Synapse2IGA(Enum):
        _300_KHZ = 0
        _1_5_MHZ = 1

    class Symphony2IGA(Enum):
        _300_KHZ = 0
        _1_5_MHZ = 1

    class SynapsePlus(Enum):
        _50_KHZ_HS = 0
        _1_MHZ_HS = 1
        _3_MHZ_HS = 2

    class SynapseEM(Enum):
        _50_KHZ_HS = 0
        _1_MHZ_HS = 1
        _3_MHZ_HS = 2
        _50_KHZ_MS = 3
        _1_MHZ_MS = 4
        _3_MHZ_MS = 5


SpeedType = Union[
    type[Speed.SyncerityOE],
    type[Speed.SyncerityNIR],
    type[Speed.SyncerityUVVis],
    type[Speed.Synapse2CCD],
    type[Speed.Symphony2CCD],
    type[Speed.Synapse2IGA],
    type[Speed.Symphony2IGA],
    type[Speed.SynapsePlus],
    type[Speed.SynapseEM],
]

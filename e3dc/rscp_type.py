from enum import Enum

_data_type_mapping = {
    "Bool": "?",
    "Char8": "b",
    "UChar8": "B",
    "Int16": "h",
    "Uint16": "H",
    "Int32": "i",
    "Uint32": "I",
    "Int64": "q",
    "Uint64": "Q",
    "Float32": "f",
    "Double64": "d",
    "Bitfield": "s",
    "CString": "s",
    "Container": "s",
    "ByteArray": "r",
    "Error": "i",
    "Nil": None,
}

class PM_TYPE(Enum):
    UNDEFINED = 0
    ROOT = 1
    ADDITIONAL = 2
    ADDITIONAL_PRODUCTION = 3
    ADDITIONAL_CONSUMPTION = 4
    FARM = 5
    UNUSED = 6
    WALLBOX = 7
    FARM_ADDITIONAL = 8

class PM_MODE(Enum):
    ACTIVE = 0
    PASSIVE = 1
    DIAGNOSE = 2
    ERROR_ACTIVE = 3
    ERROR_PASSIVE = 4

class PM_ACTIVE_PHASES(Enum):
    PHASE_100 = 1
    PHASE_010 = 2
    PHASE_110 = 3
    PHASE_001 = 4
    PHASE_101 = 5
    PHASE_011 = 6
    PHASE_111 = 7

class PVI_TYPE(Enum):
    SOLU = 1
    KACO = 2
    E3DC_E = 3

class PVI_SYSTEM_MODE(Enum):
    IDLE = 0
    NORMAL = 1
    GRIDCHARGE = 2
    BACKUPPOWER = 3

class PVI_POWER_MODE(Enum):
    ON = 1
    OFF = 0
    ON_FORCE = 101
    OFF_FORCE = 100

class EMS_GENERATOR_STATE(Enum):
    IDLE=0x00
    HEATUP=0x01
    HEATUPDONE=0x02
    STARTING=0x03
    STARTINGPAUSE=0x04
    RUNNING=0x05
    STOPPING=0x06
    STOPPED=0x07
    RELAISCONTROLMODE=0x10
    NO_GENERATOR=0xFF

class EMS_COUPLING_MODE(Enum):
    DC=0
    DC_MULTIWR=1
    AC=2
    HYBRID=3
    ISLAND=4

class EMS_SET_POWER_MODE(Enum):
    NORMAL=0
    IDLE=1
    ENTLADEN=2
    LADEN=3
    NETZLADEN=4

class EMS_EMERGENCY_POWER_STATUS(Enum):
    NOT_POSSIBLE = 0x00
    ACTIVE = 0x01
    NOT_ACTIVE = 0x02
    NOT_AVAILABLE = 0x03
    SWITCH_IN_ISLAND_STATE = 0x04

class EMS_SET_EMERGENCY_POWER(Enum):
    NORMAL_GRID_MODE = 0x00
    EMERGENCY_MODE = 0x01
    ISLAND_NO_POWER_MODE = 0x02

class WB_MODE(Enum):
    NONE = 0
    LOADING = 144 #00001001
    NOT_LOADING = 128 #00000001

class WB_TYPE(Enum):
    E3DC = 1
    EASYCONNECT = 2

class RSCP_USER_LEVEL(Enum):
    NO_AUTH = 0
    USER = 10
    INSTALLER = 20
    PARTNER = 30
    E3DC = 40
    E3DC_ADMIN = 50
    E3DC_ROOT = 60

class UM_UPDATE_STATUS(Enum):
    IDLE=0x00
    UPDATE_CHECK_RUNNING=0x01
    UPDATING_MODULES_AND_FILES=0x02
    UPDATING_HARDWARE=0x03

class ERROR_CODE(Enum):
    ERR_NOT_HANDLED=0x01
    ERR_ACCESS_DENIED=0x02
    ERR_FORMAT=0x03
    ERR_AGAIN=0x04

class RSCPType(Enum):
    Nil = 0x00
    Bool = 0x01
    Char8 = 0x02
    UChar8 = 0x03
    Int16 = 0x04
    Uint16 = 0x05
    Int32 = 0x06
    Uint32 = 0x07
    Int64 = 0x08
    Uint64 = 0x09
    Float32 = 0x0A
    Double64 = 0x0B
    Bitfield = 0x0C
    CString = 0x0D
    Container = 0x0E
    Timestamp = 0x0F
    ByteArray = 0x10
    Error = 0xFF

    @property
    def mapping(self):
        return _data_type_mapping[self.name]

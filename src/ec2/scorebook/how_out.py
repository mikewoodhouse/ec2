from enum import StrEnum

class HowOut(StrEnum):
    NOTOUT = "no"
    BOWLED = "b"
    CAUGHT = "c"
    LBW = "lbw"
    STUMPED = "st"
    RUN_OUT = "ro"
    OTHER = "other"

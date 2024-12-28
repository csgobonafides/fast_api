from enum import Enum


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class FilterType(str, Enum):
    shape = "shape"
    base = "base"
    temperature = "temperature"


class DetailType(str, Enum):
    A60 = "A60"
    C37 = "C37"
    G45 = "G45"
    R39 = "R39"
    R50 = "R50"
    R63 = "R63"
    E40 = "E40"
    E27 = "E27"
    E14 = "E14"
    ww = "ww"
    nw = "nw"
    cw = "cw"

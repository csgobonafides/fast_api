from enum import Enum, StrEnum


class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"


class FilterType(StrEnum):
    shape = "shape"
    base = "base"
    temperature = "temperature"


class ShapeType(StrEnum):
    A60 = "A60"
    C37 = "C37"
    G45 = "G45"
    R39 = "R39"
    R50 = "R50"
    R63 = "R63"


class BaseType(StrEnum):
    E40 = "E40"
    E27 = "E27"
    E14 = "E14"


class TemperatureType(StrEnum):
    ww = "ww"
    nw = "nw"
    cw = "cw"

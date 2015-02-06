"""Enumeration tools for field choices.

__new__(cls) comes from https://docs.python.org/3/library/enum.html#autonumber
"""
from enum import Enum, unique

class Choices(Enum):
    @classmethod
    def choices(cls):
        l = list(cls)
        for n in range(len(l)):
            l[n] = l[n].name, l[n].value
        return tuple(l)
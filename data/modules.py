from dataclasses import dataclass
from enum import Enum, auto

from pywa import types


class EventType(str, Enum):
    """Type of the event"""
    SHACHRIS = auto()
    SEDER_ALEF = auto()
    SEDER_BET = auto()
    SEDER_GIMEL = auto()


class Option(str, Enum):

    # USERS
    GET_EVENT_DAY = auto()
    GET_COUNT_EVENT = auto()
    GET_EVENT_SPECIFIC = auto()

    # ADMIN
    CREATE_EVENTS = auto()
    REMOVE_EVENTS = auto()
    ADD_USERS = auto()
    REMOVE_USERS = auto()
    ADD_ADMIN = auto()
    REMOVE_ADMIN = auto()

    CANCEL = auto()


@dataclass(frozen=True, slots=True)
class ChooseOption(types.CallbackData):
    choose: Option

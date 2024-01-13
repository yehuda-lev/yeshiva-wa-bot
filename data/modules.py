from dataclasses import dataclass
from enum import Enum, auto

from pywa import types


class EventType(str, Enum):
    """Type of the event"""
    SHACHRIS = auto()
    SEDER_ALEF = auto()
    SEDER_BET = auto()
    SEDER_GIMEL = auto()


class UserOption(str, Enum):

    # USERS
    GET_EVENT_DAY = auto()
    GET_COUNT_EVENT = auto()
    GET_EVENT_SPECIFIC = auto()
    HELP = auto()


@dataclass(frozen=True, slots=True)
class ChooseOptionUser(types.CallbackData):
    choose: UserOption


class AdminOption(str, Enum):
    # ADMIN

    ADMIN = auto()
    CREATE_EVENTS = auto()
    REMOVE_EVENTS = auto()
    ADD_USERS = auto()
    REMOVE_USERS = auto()
    GET_ALL_USERS = auto()
    ADD_ADMIN = auto()
    REMOVE_ADMIN = auto()

    EDIT_AND_GET_DETAILS = auto()

    USER_PAY = auto()
    USER_NOT_PAY = auto()
    USER_IN_PROGRAM = auto()
    USER_NOT_IN_PROGRAM = auto()

    CANCEL = auto()


@dataclass(frozen=True, slots=True)
class ChooseOptionAdmin(types.CallbackData):
    choose: AdminOption

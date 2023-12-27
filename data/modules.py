from dataclasses import dataclass
from enum import Enum, auto

from pywa import types


class Option(str, Enum):

    # USERS
    GET_EVENT_DAY = auto()
    GET_COUNT_EVENT = auto()
    GET_EVENT_SPECIFIC = auto()

    # ADMIN
    CREATE_EVENTS = auto()
    REMOVE_EVENTS = auto()
    ADD_USERS = auto()


@dataclass(frozen=True, slots=True)
class ChooseOption(types.CallbackData):
    choose: Option

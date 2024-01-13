import datetime
from sqlalchemy import exists, func

from db.tables import (get_session, WaUser, Event)
from data import modules

#  wa user

#  wa user


def is_wa_user_exists(*, wa_id: str) -> bool:
    """
    Check if wa user exists
    Args:
        wa_id: The WaUser ID
    Returns:
         bool
    """

    with get_session() as session:
        return session.query(exists().where(WaUser.wa_id == wa_id)).scalar()


def is_wa_user_admin(*, wa_id: str) -> bool:
    """
    Check if admin
    Args:
        wa_id: The WaUser ID
    Returns:
         bool
    """

    with get_session() as session:
        try:
            wa_user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()
            return wa_user.admin
        except AttributeError:
            return False


def get_wa_user_by_wa_id(*, wa_id: str) -> WaUser | None:
    """
    Get whatsapp user by wa_id
    Args:
        wa_id: The WaUser ID
    Returns:
         WaUser
    """

    with get_session() as session:
        wa_user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()
        return wa_user


def create_user(*, wa_id: str, name: str, admin: bool = False) -> int:
    """
    Create wa user
    Args:
        wa_id: The WaUser ID
        name: The name of user
        admin: True if user admin, (default False)
    Returns:
         id of user
    """

    with get_session() as session:
        wa_user = WaUser(
            wa_id=wa_id, name=name, admin=admin, created_at=datetime.datetime.now(),
            is_pay=False, in_program=False,
        )
        session.add(wa_user)
        session.commit()
        return wa_user.id


def update_user_info(*, wa_id: str, **kwargs):
    with get_session() as session:
        session.query(WaUser).filter(WaUser.wa_id == wa_id).update(kwargs)
        session.commit()


def del_user(*, wa_id: str):
    with get_session() as session:
        session.query(WaUser).filter(WaUser.wa_id == wa_id).delete()
        session.commit()


# event

# event

def get_event(*, wa_id: str, type_event: modules.EventType, date: datetime.date) -> Event | None:
    """
    Get event
    Args:
        wa_id: The WaUser ID of the event
        type_event: The type of the event (shachris/arvit...)
        date: The date of the event
    Returns:
         Event, if not exists return None
    """

    with get_session() as session:
        user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()

        return (
            session.query(Event)
            .where(Event.date == date)
            .where(Event.type == type_event)
            .where(Event.by_wa_user_id == user.id)
            .first()
        )


def create_event(*, type_event: modules.EventType, date: datetime.date, wa_id: str, added_by: str) -> int:
    """
    Create event
    Args:
        type_event: The type of the event (shachris/arvit...)
        date: The date of the event
        wa_id: The WaUser ID of the event
        added_by: The name of the admin the create the event
    Returns:
         id of the event
    """

    with get_session() as session:
        user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()

        event = Event(type=type_event, date=date, by_wa_user_id=user.id, added_by_admin=added_by)
        session.add(event)
        session.commit()
        return event.id


def del_event(*, wa_id: str, type_event: modules.EventType, date: datetime.date) -> None:
    """
    Del event
    Args:
        wa_id: The WaUser ID of the event
        type_event: The type of the event (shachris/arvit...)
        date: The date of the event
    Returns:
         None
    """

    with get_session() as session:
        user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()

        return (
            session.query(Event)
            .where(Event.date == date)
            .where(Event.type == type_event)
            .where(Event.by_wa_user_id == user.id)
            .delete()
        )

# admin

# admin


def get_all_users(pay: bool = None, in_program: bool = None, is_admin: bool = None) -> dict[str, tuple[str, int]]:
    """
    Get all users
    Args:
        pay: if user pay or not (default None)
        in_program: if user in the program or not (default None)
        is_admin: if user is admin or not (default None)
    Returns:
         dict[wa_id: tuple[name, id]]
    """

    with get_session() as session:
        users = session.query(
            WaUser
        ).filter(  # filter is_pay
            WaUser.is_pay == pay
            if pay is not None
            else True,
        ).filter(  # filter in_program
            WaUser.in_program == in_program
            if in_program is not None
            else True,
        ).filter(  # filter is_admin
            WaUser.admin == is_admin
            if is_admin is not None
            else True,
        )
        dict_users = {}
        for user in users:
            dict_users.update({user.wa_id: (user.name, user.id)})

        return dict_users


# users

# users

def get_events_count_by_wa_id(*, wa_id: str, type_event: modules.EventType = None, date: datetime.date = None) -> int:
    """
    Get count events of wa user
    Args:
        wa_id: The WaUser ID of the event
        type_event: The type of the event (shachris/arvit...), default None
        date: The date of the event, default None
    Returns:
         count events
    """

    with get_session() as session:
        user = session.query(WaUser).filter(WaUser.wa_id == wa_id).first()

        return session.query(
            func.count(Event.id)
            .filter(Event.by_wa_user_id == user.id)
            .filter(  # filter date
                Event.date == date
                if date is not None
                else True,
            )
            .filter(  # filter type
                Event.type == type_event
                if type_event is not None
                else True,
            )
        ).scalar()

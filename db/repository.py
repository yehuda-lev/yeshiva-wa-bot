import datetime
from sqlalchemy import exists

from db.tables import (get_session, WaUser, Event, EventType)


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
        wa_user = WaUser(wa_id=wa_id, name=name, admin=admin, created_at=datetime.datetime.now())
        session.add(wa_user)
        session.commit()
        return wa_user.id


# event

# event

def get_event(*, wa_id: str, type_event: EventType, date: datetime.date) -> Event | None:
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


def create_event(*, type_event: EventType, date: datetime.date, wa_id: str, added_by: str) -> int:
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

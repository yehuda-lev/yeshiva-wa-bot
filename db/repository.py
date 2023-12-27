import datetime
from sqlalchemy import exists

from db.tables import (get_session, WaUser, Event, EventType)


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
        wa_user = WaUser(wa_id=wa_id, name=name, admin=admin, creat_at=datetime.datetime.now())
        session.add(wa_user)
        session.commit()
        return wa_user.id

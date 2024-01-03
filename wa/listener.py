
user_id_to_state: dict[str: dict] = {}
"""example: {wa_id: {remove_user}}"""


def status_answer(*, wa_id: str) -> bool:
    exists = user_id_to_state.get(wa_id)
    if exists:
        return True
    return False


def add_listener(*, wa_id: str, data: dict):
    """example: {9721234567: {add_users}}"""
    user_id_to_state.update({wa_id: data})


def remove_listener(*, wa_id: str):
    try:
        user_id_to_state.pop(wa_id)
    except KeyError:
        pass

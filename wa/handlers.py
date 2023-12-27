from pywa import handlers, filters, WhatsApp, types

from db import repository
from wa import start


def filter_exists(_: WhatsApp, msg: types.Message) -> bool:
    """is user exists"""

    msg.mark_as_read()
    wa_id = msg.from_user.wa_id

    return repository.is_wa_user_exists(wa_id=wa_id)


HANDLERS = [
    handlers.MessageHandler(
        start.send_welcome,
        filter_exists,
        filters.text
    )
]

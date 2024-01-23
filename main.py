import logging
import uvicorn
from fastapi import FastAPI
from pywa import WhatsApp, filters, types

from wa import handlers
from data.utils import get_settings
from db import repository


# log config
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
file_handler = logging.handlers.RotatingFileHandler(
    filename="bot.log", maxBytes=5 * (2**20), backupCount=1, mode="D"
)
file_handler.setLevel(logging.INFO)
logging.basicConfig(
    format="Time: %(asctime)s | Level: %(levelname)s | Module: %(module)s | Message: %(message)s",
    handlers=(console_handler, file_handler),
)
logging.getLogger().setLevel(logging.NOTSET)
_logger = logging.getLogger(__name__)


app = FastAPI()
settings = get_settings()

wa = WhatsApp(
    phone_id=settings.WA_PHONE_ID,
    token=settings.WA_TOKEN,
    business_account_id=settings.WA_BUSINESS_ID,
    server=app,
    verify_token=settings.WA_VERIFY_TOKEN,
    callback_url=settings.CALLBACK_URL,
    webhook_endpoint=settings.WEBHOOK_ENDPOINT,
    app_id=int(settings.APP_ID),
    app_secret=settings.APP_SECRET,
    business_private_key=settings.PRIVATE_KEY,
    business_private_key_password=settings.PASSWORD_PRIVATE_KEY,
    verify_timeout=10,
)


@wa.on_message_status(filters.message_status.failed)
def on_failed_message(_: WhatsApp, status: types.MessageStatus):
    wa_id = status.from_user.wa_id
    _logger.error(f"Message failed to send to {wa_id} with error: {status.error}")


#  add handlers
for handler in handlers.HANDLERS:
    wa.add_handlers(handler)


# add admins
for admin in settings.ADMINS.split(","):
    if not repository.is_wa_user_exists(wa_id=admin):
        repository.create_user(wa_id=admin, name="admin", admin=True)
    else:
        if not repository.is_wa_user_admin(wa_id=admin):
            repository.update_user_info(user_wa_id=admin, admin=True)


uvicorn.run(app, port=8080, access_log=False)

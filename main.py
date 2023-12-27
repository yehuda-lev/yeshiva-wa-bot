import uvicorn
from fastapi import FastAPI
from pywa import WhatsApp

from wa import handlers
from data.utils import get_settings


app = FastAPI()

settings = get_settings()

wa = WhatsApp(
    phone_id=settings.WA_PHONE_ID,
    token=settings.WA_TOKEN,
    business_account_id=settings.WA_BUSINESS_ID,
    server=app,
    verify_token=settings.WA_VERIFY_TOKEN,
    callback_url=settings.CALLBACK_URL,
    app_id=int(settings.APP_ID),
    app_secret=settings.APP_SECRET,
    business_private_key=settings.PRIVATE_KEY,
    business_private_key_password=settings.PASSWORD_PRIVATE_KEY,
    verify_timeout=10,
)


#  add handlers
for handler in handlers.HANDLERS:
    wa.add_handlers(handler)


uvicorn.run(app, port=8080, access_log=False)

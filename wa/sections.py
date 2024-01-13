from pywa import WhatsApp, types
import datetime

from pywa.types import flows

from db import repository
from data import modules, utils
from wa import listener, helpers

settings = utils.get_settings()


def get_event_per_day(wa_id: str, date: datetime.date.today) -> str:
    shahris = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SHACHRIS, date=date)
    seder_a = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_ALEF, date=date)
    seder_b = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_BET, date=date)
    seder_g = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_GIMEL, date=date)

    return (f'למדת בתאריך {date}:\n'
            f'שחרית: {"❌" if shahris is None else "✅"}\n'
            f'סדר א: {"❌" if seder_a is None else "✅"}\n'
            f'סדר ב: {"❌" if seder_b is None else "✅"}\n'
            f'סדר ג: {"❌" if seder_g is None else "✅"}\n')


def get_event_day(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionUser]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    date = datetime.date.today()

    cbs.reply(
        text=get_event_per_day(wa_id=wa_id, date=date)
    )


def get_count_event(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionUser]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    text_data = helpers.get_data_by_user(wa_id=wa_id)
    cbs.reply(text=f"למדת \n{text_data}")


def get_event_specific(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionUser]):
    cbs.reply(
        text='יצירת אירוע',
        buttons=types.FlowButton(
            title='יצירת אירוע',
            flow_id=settings.FLOW_ID,
            flow_action_type=flows.FlowActionType.NAVIGATE,
            flow_token=f'get_event_specific_{cbs.from_user.wa_id}',
            mode=settings.FLOW_STATUS,
            flow_action_screen='choose_date_and_type',
            flow_action_payload={
                "welcome_user": f"שלום {cbs.from_user.name}",
                "is_event_type_required": False,
            }
        )
    )


# admin

def add_and_remove_events(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionAdmin]):
    cbs.mark_as_read()

    is_create = cbs.data.choose == modules.AdminOption.CREATE_EVENTS

    cbs.reply(
        text=f"נא ללחוץ על הכפתור למטה בכדי{'להוסיף' if is_create else 'להסיר'} אירועים",
        buttons=types.FlowButton(
            title='open',
            flow_id=settings.FLOW_ID,
            flow_action_type=flows.FlowActionType.NAVIGATE,
            flow_token=f'{"add" if is_create else "remove"}_events_{cbs.from_user.wa_id}',
            mode=settings.FLOW_STATUS,
            flow_action_screen='choose_date_and_type',
            flow_action_payload={
                "welcome_user": f"ברוך הבא {cbs.from_user.name}",
                "is_event_type_required": True,
                # "default_date": str(int(datetime.datetime.today().timestamp())),
                # "default_date": datetime.datetime.today().timestamp(),
            }
        )
    )


def add_users(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionAdmin]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    # add listener
    listener.add_listener(
        wa_id=wa_id,
        data={"add_users": True}
    )

    cbs.reply(
        text="אנא שלח לי את האנשי קשר שברצונך להוסיף",
        buttons=[
            types.Button(title="ביטול", callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.CANCEL))
        ]
    )


def handle_user_details(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionAdmin]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    cbs.reply(
        text='אנא לחץ על הכפתור למטה בכדי לקבל או לערוך את פרטי המשתמשים',
        buttons=types.FlowButton(
            title='ניהול משתמשים',
            flow_id=settings.FLOW_ID,
            flow_action_type=flows.FlowActionType.NAVIGATE,
            flow_token=f"get_user_details_{wa_id}",
            mode=settings.FLOW_STATUS,
            flow_action_screen='user_details',
            flow_action_payload={
                "data_ask_user_details": [
                    {
                        "id": modules.AdminOption.USER_IN_PROGRAM,
                        "title": "משתמשים שבמבצע",
                    },
                    {
                        "id": modules.AdminOption.USER_NOT_IN_PROGRAM,
                        "title": "משתמשים שלא במבצע",
                    },
                    {
                        "id": modules.AdminOption.USER_PAY,
                        "title": "משתמשים ששילמו",
                    },
                    {
                        "id": modules.AdminOption.USER_NOT_PAY,
                        "title": "משתמשים שלא שילמו",
                    }, {
                        "id": modules.AdminOption.GET_ALL_USERS,
                        "title": "כל המשתמשים",
                    },
                    {
                        "id": modules.AdminOption.REMOVE_USERS,
                        "title": "מחיקת משתמשים מהבוט",
                    },
                    {
                        "id": modules.AdminOption.ADD_ADMIN,
                        "title": "משתמשים שלא מנהלים",
                    },
                    {
                        "id": modules.AdminOption.REMOVE_ADMIN,
                        "title": "משתמשים שמנהלים",
                    },
                    {
                        "id": modules.AdminOption.GET_STATS,
                        "title": "סטטיסטיקת לימוד",
                    },
                ]
            }
        )
    )


def send_help(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionAdmin]):
    cbs.mark_as_read()
    text = """*עזרה*\n
    עד יום חמישי הסמוך לטיסה יש 10 שבועות שהם:
50 תפילות שחרית
50 סדרי א’
40 סדרי ב’ 
40סדרי ג’
סך הכל 180 זכויות.
בהשתתפות ב 140 זכויות (מה שתבחרו)  הנכם זכאים להשתתף בטיול בעלות של 1300 ש’’ח בלבד.
בהשתתפות של בין 100 ל140 זכויות הנכם זכאים להשתתף בטיול בעלות של 2000 שקלים בלבד. 
בהשתתפות של בין 70 ל100 זכויות הנכם זכאים להשתתף בטיול בעלות של 2550 שקלים.
9.בהשתתפות של פחות מ70 זכויות הנכם נדרשים לשלם מחיר מלא בסך 3800 שקלים 
מחיר זה תקף לבני הישיבה בלבד, אורחים מחוץ לישיבה יצטרכו לשלם יותר עקב עלייה חדה במחירי הטיסות והאטרקציות.
"""
    cbs.reply(text)

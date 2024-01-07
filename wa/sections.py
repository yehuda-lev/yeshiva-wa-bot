from pywa import WhatsApp, types
import datetime

from pywa.types import flows

from db import repository
from data import modules, utils
from wa import listener

settings = utils.get_settings()


def get_event_peer_day(wa_id: str, date: datetime.date.today) -> str:
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
        text=get_event_peer_day(wa_id=wa_id, date=date)
    )


def get_count_event(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionUser]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    shahris = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SHACHRIS)
    seder_a = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_ALEF)
    seder_b = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_BET)
    seder_g = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_GIMEL)

    cbs.reply(
        text=f'למדת:\n'
             f'שחרית: {shahris}\n'
             f'סדר א: {seder_a}\n'
             f'סדר ב: {seder_b}\n'
             f'סדר ג: {seder_g}\n'
             f'הכל ביחד: {shahris + seder_a + seder_b + seder_g}'
    )


def get_event_specific(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionUser]):
    cbs.reply(
        text='יצירת אירוע',
        buttons=types.FlowButton(
            title='יצירת אירוע',
            flow_id=settings.FLOW_ID,
            flow_action_type=flows.FlowActionType.NAVIGATE,
            flow_token=f'get_event_specific_{cbs.from_user.wa_id}',
            mode=flows.FlowStatus.DRAFT,
            flow_action_screen='choose_date_and_type',
            flow_action_payload={
                "welcome_user": f"Hello {cbs.from_user.name}",
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
            mode=flows.FlowStatus.DRAFT,
            flow_action_screen='choose_date_and_type',
            flow_action_payload={
                "welcome_user": f"ברוך הבא {cbs.from_user.name}",
                "is_event_type_required": True,
                # "default_date": str(int(datetime.datetime.today().timestamp())),
                # "default_date": datetime.datetime.today().timestamp(),
            }
        )
    )


def add_and_remove_users(
        _: WhatsApp, cbs:
        types.CallbackSelection[modules.ChooseOptionAdmin] | types.CallbackButton[modules.ChooseOptionAdmin]):
    wa_id = cbs.from_user.wa_id

    callback_data = cbs.data.choose

    cbs.mark_as_read()

    add_users = callback_data == modules.AdminOption.ADD_USERS or callback_data == modules.AdminOption.ADD_ADMIN

    admin = None
    if callback_data == modules.AdminOption.ADD_ADMIN:
        admin = True
    elif callback_data == modules.AdminOption.REMOVE_ADMIN:
        admin = False

    # add listener
    listener.add_listener(
        wa_id=wa_id,
        data={
            "add_users": True if add_users else False,
            "admin": admin
        }
    )

    text_admin = None
    match callback_data:
        case modules.AdminOption.ADD_USERS:
            text = "אנא שלח לי את האנשי קשר שברצונך להוסיף"
            text_admin = "להוספת מנהל"

        case modules.AdminOption.REMOVE_USERS:
            text = "אנא שלח לי את האנשי קשר שברצונך להסיר"
            text_admin = "להסרת מנהל"

        case modules.AdminOption.ADD_ADMIN:
            text = "אנא שלח לי את האנשי קשר שברצונך להוסיף לניהול"

        case modules.AdminOption.REMOVE_ADMIN:
            text = "אנא שלח לי את האנשי קשר שברצונך להסיר מהניהול"
        case _:
            return

    buttons = [
        types.Button(title="ביטול", callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.CANCEL))
    ]
    if admin is None:
        buttons.append(
            types.Button(title=text_admin, callback_data=modules.ChooseOptionAdmin(
                choose=modules.AdminOption.ADD_ADMIN
                if callback_data == modules.AdminOption.ADD_USERS else modules.AdminOption.REMOVE_ADMIN))
        )

    cbs.reply(
        text=text,
        buttons=buttons
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
            mode=flows.FlowStatus.DRAFT,
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

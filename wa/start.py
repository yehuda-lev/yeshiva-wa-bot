from pprint import pprint

from pywa import WhatsApp, types

from db import repository
from data import modules
from wa import listener


def send_welcome(_: WhatsApp, msg: types.Message):
    wa_id = msg.from_user.wa_id

    sections = [
        types.SectionRow(
            title='כמה למדתי היום',
            callback_data=modules.ChooseOptionUser(choose=modules.UserOption.GET_EVENT_DAY)
        ),
        types.SectionRow(
            title='כמה למדתי במשך כל המבצע',
            callback_data=modules.ChooseOptionUser(choose=modules.UserOption.GET_COUNT_EVENT)
        ),
        types.SectionRow(
            title='חיפוש לפי יום',
            callback_data=modules.ChooseOptionUser(choose=modules.UserOption.GET_EVENT_SPECIFIC)
        ),
    ]

    if repository.is_wa_user_admin(wa_id=wa_id):
        sections.append(
            types.SectionRow(
                title='הגדרות מנהל',
                callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.ADMIN)
            )
        )

    msg.reply(
        text=f'ברוך הבא {msg.from_user.name} לבוט',
        footer='יהודה לב - צ`אטבוטים ואוטומציה',
        buttons=types.SectionList(
            button_title='בחר',
            sections=[
                types.Section(
                    title='בחר',
                    rows=sections
                ),
            ]
        )
    )


def admin_selection(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOptionAdmin]):
    cbs.mark_as_read()

    sections = [
        types.SectionRow(
            title='יצירת אירוע',
            callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.CREATE_EVENTS)
        ),
        types.SectionRow(
            title='מחיקת אירוע',
            callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.REMOVE_EVENTS)
        ),
        types.SectionRow(
            title='הוספת משתמשים חדשים',
            callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.ADD_USERS)
        ),
        types.SectionRow(
            title='מחיקת משתמשים',
            callback_data=modules.ChooseOptionAdmin(choose=modules.AdminOption.REMOVE_USERS)
        ),
    ]

    cbs.reply(
        text=f'הגדרות מנהל',
        buttons=types.SectionList(
            button_title='בחר',
            sections=[
                types.Section(
                    title='בחר',
                    rows=sections
                ),
            ]
        )
    )


def handle_contact(_: WhatsApp, msg: types.Message):
    wa_id = msg.from_user.wa_id

    get_data = listener.user_id_to_state[wa_id]

    is_admin = get_data["admin"]
    admin = True if is_admin is True else False

    users = ""
    for contact in msg.contacts:
        for number in contact.phones:
            phone = number.wa_id if number.wa_id else number.phone
            name = contact.name.formatted_name
            if not repository.is_wa_user_exists(wa_id=phone):
                repository.create_user(wa_id=phone, name=name, admin=admin)
                users += f"{name}\n"

            else:
                if get_data["add_users"]:
                    if is_admin is not None:
                        repository.update_user_info(wa_id=phone, admin=admin)
                        users += f"{name}\n"
                else:
                    repository.del_user(wa_id=phone)

    listener.remove_listener(wa_id=wa_id)

    if len(users) != 0:
        msg.reply(
            text=users
        )


def cancel(_: WhatsApp, cbd: types.CallbackButton[modules.ChooseOptionAdmin]):
    wa_id = cbd.from_user.wa_id
    listener.remove_listener(wa_id=wa_id)
    cbd.reply(text="בוצע")

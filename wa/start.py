from pywa import WhatsApp, types

from db import repository
from data import modules


def send_welcome(_: WhatsApp, msg: types.Message):
    wa_id = msg.from_user.wa_id

    users_sections = [
        types.SectionRow(
            title='get event day',
            description='get the events of the day',
            callback_data=modules.ChooseOption(choose=modules.Option.GET_EVENT_DAY)
        ),
        types.SectionRow(
            title='get count event',
            description='get the count of all my events',
            callback_data=modules.ChooseOption(choose=modules.Option.GET_COUNT_EVENT)
        ),
        types.SectionRow(
            title='get event specific',
            description='get specific event',
            callback_data=modules.ChooseOption(choose=modules.Option.GET_EVENT_SPECIFIC)
        ),
    ]

    admin_sections = [
        types.SectionRow(
            title='create events',
            callback_data=modules.ChooseOption(choose=modules.Option.CREATE_EVENTS)
        ),
        types.SectionRow(
            title='remove events',
            callback_data=modules.ChooseOption(choose=modules.Option.REMOVE_EVENTS)
        ),
        types.SectionRow(
            title='add users',
            description='added new users',
            callback_data=modules.ChooseOption(choose=modules.Option.ADD_USERS)
        ),
    ]

    sections = [
        types.Section(
            title='choose one section',
            rows=users_sections
        ),
    ]

    if repository.is_wa_user_admin(wa_id=wa_id):
        sections.append(
            types.Section(
                title='admins options',
                rows=admin_sections
            )
        )

    msg.reply(
        text=f'welcome {msg.from_user.name} to the bot...',
        footer='Power by yehudalev',
        buttons=types.SectionList(
            button_title='Choose',
            sections=sections
        )
    )

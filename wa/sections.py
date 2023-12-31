from pywa import WhatsApp, types
import datetime

from pywa.types import flows

from db import repository
from data import modules


def get_event_day(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOption]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    date = datetime.datetime.now()

    # TODO not working

    shahris = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SHACHRIS, date=date)
    seder_a = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_ALEF, date=date)
    seder_b = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_BET, date=date)
    seder_g = repository.get_event(wa_id=wa_id, type_event=modules.EventType.SEDER_GIMEL, date=date)

    cbs.reply(
        text=f'למדת:\n'
             f'shachris: {"X" if shahris is None else "V"}\n'
             f'seder a: {"X" if seder_a is None else "V"}\n'
             f'seder b: {"X" if seder_b is None else "V"}\n'
             f'seder g: {"X" if seder_g is None else "V"}\n'
    )


def get_count_event(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOption]):
    cbs.mark_as_read()
    wa_id = cbs.from_user.wa_id

    shahris = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SHACHRIS)
    seder_a = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_ALEF)
    seder_b = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_BET)
    seder_g = repository.get_events_count_by_wa_id(wa_id=wa_id, type_event=modules.EventType.SEDER_GIMEL)

    cbs.reply(
        text=f'למדת:\n'
             f'shachris: {shahris}\n'
             f'seder a: {seder_a}\n'
             f'seder b: {seder_b}\n'
             f'seder g: {seder_g}\n'
             f'all: {shahris + seder_a + seder_b + seder_g}'
    )


def get_event_specific(_: WhatsApp, cbs: types.CallbackSelection[modules.ChooseOption]):
    cbs.reply(
        text='this is a test with Flow',
        buttons=types.FlowButton(
            title='test flow',
            flow_id=774420634511632,
            flow_action_type=flows.FlowActionType.NAVIGATE,
            flow_token=f'choose_date_and_type_{cbs.from_user.wa_id}',
            mode=flows.FlowStatus.DRAFT,
            flow_action_screen='choose_date_and_type',
            flow_action_payload={
                "welcome_user": f"Hello {cbs.from_user.name}",
                "is_event_type_required": False,
                "is_date_required": True,
            }
        )
    )

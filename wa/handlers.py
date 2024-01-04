from pywa import handlers, filters, WhatsApp, types

from db import repository
from wa import start, sections, handale_flows, listener
from data import modules


def filter_exists(_: WhatsApp, msg: types.Message) -> bool:
    """is user exists"""

    msg.mark_as_read()
    wa_id = msg.from_user.wa_id

    return repository.is_wa_user_exists(wa_id=wa_id)


HANDLERS = [
    handlers.MessageHandler(
        start.send_welcome,
        filter_exists,
        filters.text,
        filters.not_(filters.text.is_command)
    ),

    handlers.MessageHandler(
        start.handle_contact,
        filter_exists,
        filters.contacts,
        lambda _, msg: listener.status_answer(wa_id=msg.from_user.wa_id)
    ),

    # callback selection
    handlers.CallbackSelectionHandler(
        sections.get_event_day,
        lambda _, cbs: cbs.data.choose == modules.Option.GET_EVENT_DAY,
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),
    handlers.CallbackSelectionHandler(
        sections.get_count_event,
        lambda _, cbs: cbs.data.choose == modules.Option.GET_COUNT_EVENT,
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),
    handlers.CallbackSelectionHandler(
        sections.get_event_specific,
        lambda _, cbs: cbs.data.choose == modules.Option.GET_EVENT_SPECIFIC,
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),
    # admin
    handlers.CallbackSelectionHandler(
        sections.add_and_remove_events,
        lambda _, cbs: (cbs.data.choose == modules.Option.CREATE_EVENTS
                        or cbs.data.choose == modules.Option.REMOVE_EVENTS),
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),
    handlers.CallbackSelectionHandler(
        sections.add_and_remove_users,
        lambda _, cbs: (cbs.data.choose == modules.Option.ADD_USERS
                        or cbs.data.choose == modules.Option.REMOVE_USERS),
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),

    # flows
    handlers.FlowRequestHandler(
        handale_flows.get_request_flow,
        endpoint='/support_request_flow',
    ),

    handlers.FlowCompletionHandler(
        handale_flows.get_completion_flow,
    ),

    # callback button
    handlers.CallbackButtonHandler(
        sections.add_and_remove_users,
        lambda _, cbd: (cbd.data.choose == modules.Option.ADD_ADMIN
                        or cbd.data.choose == modules.Option.REMOVE_ADMIN),
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),

    handlers.CallbackButtonHandler(
        start.cancel,
        lambda _, cbd: cbd.data.choose == modules.Option.CANCEL,
        factory_before_filters=True,
        factory=modules.ChooseOption,
    ),
]

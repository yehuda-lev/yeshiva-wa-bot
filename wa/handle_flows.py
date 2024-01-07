import datetime
import logging

from pywa import WhatsApp, types
from pywa.types import flows
from pprint import pprint

from data import modules
from db import repository
from wa import sections, helpers


def get_request_flow(_: WhatsApp, req: flows.FlowRequest) -> flows.FlowResponse | None:

    if req.has_error:
        logging.error(f"Request has err: {req.data}")
        return

    flow_token = req.flow_token

    if flow_token.startswith("get_event_specific"):
        return flows.FlowResponse(
            version=req.version,
            close_flow=True,
            flow_token=req.flow_token,
            data={
                **req.data,
            }
        )

    elif flow_token.startswith("get_user_details"):
        res = req.data

        # get_user = modules.AdminOption[res["get_user"]]
        get_user = list(modules.AdminOption)[int(res["get_user"]) - 1]
        print(get_user)

        filter_pay, filter_program = None, None

        match get_user:
            case modules.AdminOption.USER_PAY:
                filter_pay = True
            case modules.AdminOption.USER_NOT_PAY:
                filter_pay = False
            case modules.AdminOption.USER_IN_PROGRAM:
                filter_program = True
            case modules.AdminOption.USER_NOT_IN_PROGRAM:
                filter_program = False
            case _:
                return

        return flows.FlowResponse(
            version=req.version,
            close_flow=False,
            flow_token=req.flow_token,
            screen="choose_people",
            data={
                "event_type": "None",
                "date": "None",
                **req.data,
                **helpers.get_data_users(filter_in_program=filter_program, filter_pay=filter_pay)
            }
        )

    else:
        return flows.FlowResponse(
            version=req.version,
            close_flow=False,
            flow_token=req.flow_token,
            screen="choose_people",
            data={
                **req.data,
                **helpers.get_data_users(filter_in_program=True),
                "type_get_user": ["none"],
                "get_user": "none",
            }
        )


def get_completion_flow(_: WhatsApp, flow: types.FlowCompletion):
    flow.mark_as_read()
    wa_id = flow.from_user.wa_id
    res = flow.response

    if flow.token.startswith('add_events') or flow.token.startswith('remove_events'):

        event_type = modules.EventType[res["event_type"]]

        date = datetime.date.fromtimestamp(int(res["date"]) / 1000)

        list_users = ""

        for users in res["people_group_1"], res["people_group_2"], res["people_group_3"], res["people_group_4"]:
            for user in users:
                if repository.is_wa_user_exists(wa_id=user):
                    exists = repository.get_event(
                        wa_id=user,
                        type_event=event_type,
                        date=date
                    )

                    if exists is None:
                        # add events
                        if flow.token.startswith('add_events'):
                            repository.create_event(
                                type_event=event_type,
                                date=date,
                                wa_id=user,
                                added_by=flow.from_user.name
                            )
                            list_users += f"{repository.get_wa_user_by_wa_id(wa_id=user).name}\n"

                    else:
                        if flow.token.startswith('remove_events'):
                            repository.del_event(type_event=event_type, date=date, wa_id=user)
                            list_users += f"{repository.get_wa_user_by_wa_id(wa_id=user).name}\n"

        event_type_he = ""
        match event_type:
            case modules.EventType.SHACHRIS:
                event_type_he = "שחרית"
            case modules.EventType.SEDER_ALEF:
                event_type_he = "סדר א"
            case modules.EventType.SEDER_BET:
                event_type_he = "סדר ב"
            case modules.EventType.SEDER_GIMEL:
                event_type_he = "סדר ג"

        if flow.token.startswith('remove_events'):
            text = f"למשתמשים הבאים הוסרו האירועים '{event_type_he}' לפי תאריך {date}\n{list_users}"

        elif flow.token.startswith('add_events'):
            text = f"למשתמשים הבאים נוספו האירועים '{event_type_he}' לפי תאריך {date}\n{list_users}"
        else:
            return

        if len(list_users) != 0:
            flow.reply(
                text=text
            )

    elif flow.token.startswith('get_event_specific'):
        date = datetime.date.fromtimestamp(int(res["date"]) / 1000)

        flow.reply(
            text=sections.get_event_peer_day(wa_id=wa_id, date=date)
        )

    elif flow.token.startswith("get_user_details"):

        type_get_user = res["data_type_get_user"][0]
        get_user = list(modules.AdminOption)[int(res["data_get_user"]) - 1]

        if type_get_user == "get_info":
            info_users = ""

            for users in res["people_group_1"], res["people_group_2"], res["people_group_3"], res["people_group_4"]:
                for user in users:
                    if repository.is_wa_user_exists(wa_id=user):
                        wa_user = repository.get_wa_user_by_wa_id(wa_id=user)
                        info_users += wa_user.name
            if len(info_users) != 0:
                flow.reply(info_users)

        else:
            info_users = ""

            for users in res["people_group_1"], res["people_group_2"], res["people_group_3"], res["people_group_4"]:
                for user in users:
                    if repository.is_wa_user_exists(wa_id=user):
                        match get_user:
                            case modules.AdminOption.USER_PAY:
                                repository.update_user_info(wa_id=user, is_pay=False)
                            case modules.AdminOption.USER_NOT_PAY:
                                repository.update_user_info(wa_id=user, is_pay=True)
                            case modules.AdminOption.USER_IN_PROGRAM:
                                repository.update_user_info(wa_id=user, in_program=False)
                            case modules.AdminOption.USER_NOT_IN_PROGRAM:
                                repository.update_user_info(wa_id=user, in_program=True)
                            case _:
                                return
                        wa_user = repository.get_wa_user_by_wa_id(wa_id=user)
                        info_users += wa_user.name

            if len(info_users) != 0:
                flow.reply(info_users)

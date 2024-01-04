import datetime
import logging
import re

from pywa import WhatsApp, types
from pywa.types import flows
from pprint import pprint

from data import modules
from db import repository
from wa import sections


def get_data_users() -> list[dict]:
    return [
        {
            "id": k,
            "title": v[0],
            "description": re.sub("^972", "0", k)}
        for k, v in repository.get_all_users().items()]


def get_data_source(index: int, list_users: list) -> list[dict]:
    data_source = []

    for user in list_users[index: (index + 20)]:
        data_source.append(
            user
        )
    if len(data_source) == 0:
        data_source.append({"id": "0"})
    return data_source


def get_request_flow(_: WhatsApp, req: flows.FlowRequest) -> flows.FlowResponse | None:

    if req.has_error:
        logging.error(f"Request has err: {req.data}")
        return
    if req.flow_token.startswith("get_event_specific"):
        return flows.FlowResponse(
            version=req.version,
            close_flow=True,
            flow_token=req.flow_token,
            data={
                **req.data,
            }
        )

    all_users = get_data_users()

    is_group_1_visible = False
    is_group_2_visible = False
    is_group_3_visible = False
    is_group_4_visible = False

    people_group_1 = get_data_source(index=0, list_users=all_users)
    people_group_2 = get_data_source(index=20, list_users=all_users)
    people_group_3 = get_data_source(index=40, list_users=all_users)
    people_group_4 = get_data_source(index=60, list_users=all_users)

    if len(all_users) > 0:
        is_group_1_visible = True
    if len(all_users) > 20:
        is_group_2_visible = True
    if len(all_users) > 40:
        is_group_3_visible = True
    if len(all_users) > 60:
        is_group_4_visible = True

    return flows.FlowResponse(
        version=req.version,
        close_flow=False,
        flow_token=req.flow_token,
        screen="choose_people",
        data={
            **req.data,
            "data_people_group_1": people_group_1,
            "data_is_group_1_visible": is_group_1_visible,
            "data_people_group_2": people_group_2,
            "data_is_group_2_visible": is_group_2_visible,
            "data_people_group_3": people_group_3,
            "data_is_group_3_visible": is_group_3_visible,
            "data_people_group_4": people_group_4,
            "data_is_group_4_visible": is_group_4_visible
        }
    )


def get_completion_flow(_: WhatsApp, flow: types.FlowCompletion):
    flow.mark_as_read()
    wa_id = flow.from_user.wa_id

    if flow.token.startswith('add_events') or flow.token.startswith('remove_events'):

        res = flow.response

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

        if flow.token.startswith('remove_events'):
            text = f"למשתמשים הבאים הוסרו האירועים {res['event_type']} לפי תאריך {date}\n{list_users}"

        elif flow.token.startswith('add_events'):
            text = f"למשתמשים הבאים נוספו האירועים {res['event_type']} לפי תאריך {date}\n{list_users}"
        else:
            return

        if len(list_users) != 0:
            flow.reply(
                text=text
            )

    elif flow.token.startswith('get_event_specific'):
        res = flow.response
        date = datetime.date.fromtimestamp(int(res["date"]) / 1000)

        flow.reply(
            text=sections.get_event_peer_day(wa_id=wa_id, date=date)
        )

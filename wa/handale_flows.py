import datetime
import logging
import re

from pywa import WhatsApp, types
from pywa.types import flows
from pprint import pprint

from data import modules
from db import repository


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
    return data_source


def get_request_flow(_: WhatsApp, req: flows.FlowRequest) -> flows.FlowResponse | None:
    pprint(req)

    if req.has_error:
        logging.error(f"Request has err: {req.data}")
        return
    if req.flow_token.startswith("choose_date_and_type"):
        return flows.FlowResponse(
            version=req.version,
            close_flow=True,
            flow_token=req.flow_token,
            data={
                **req.data,
            }
        )

    all_users = get_data_users()

    is_group_4_enabled = False
    people_group_4 = []

    people_group_1 = get_data_source(index=0, list_users=all_users)
    people_group_2 = get_data_source(index=20, list_users=all_users)
    people_group_3 = get_data_source(index=40, list_users=all_users)

    if len(all_users) > 60:
        people_group_4 = get_data_source(index=60, list_users=all_users)
        is_group_4_enabled = True

    return flows.FlowResponse(
        version=req.version,
        close_flow=False,
        flow_token=req.flow_token,
        screen="choose_people",
        data={
            **req.data,
            "data_people_group_1": people_group_1,
            "data_people_group_2": people_group_2,
            "data_people_group_3": people_group_3,
            "data_people_group_4": people_group_4,
            "data_is_group_4_enabled": is_group_4_enabled
        }
    )


def get_completion_flow(_: WhatsApp, flow: types.FlowCompletion):
    flow.mark_as_read()
    wa_id = flow.from_user.wa_id

    pprint(flow)

    if flow.token.startswith('add_events') or flow.token.startswith('remove_events'):

        res = flow.response

        event_type = modules.EventType[res["event_type"]]

        date = datetime.date.fromtimestamp(int(res["date"]) / 1000)

        list_users = ""

        for users in res["people_group_1"], res["people_group_2"], res["people_group_3"], res["people_group_4"]:
            for user in users:
                wa_id = user

                exists = repository.get_event(
                    wa_id=wa_id,
                    type_event=event_type,
                    date=date
                )

                if exists is None:
                    # add events
                    if flow.token.startswith('add_events'):
                        repository.create_event(
                            type_event=event_type,
                            date=date,
                            wa_id=wa_id,
                            added_by=flow.from_user.name
                        )
                        list_users += f"{repository.get_wa_user_by_wa_id(wa_id=wa_id).name}\n"

                else:
                    if flow.token.startswith('remove_events'):
                        pass
                        # TODO remove users
                        # repository.delete_event(
                        #     type_event=event_type,
                        #     date=date,
                        #     wa_id=wa_id,
                        #     added_by=flow.from_user.name
                        # )
                        # list_users += f"{repository.get_wa_user_by_wa_id(wa_id=wa_id).name}\n"

        if len(list_users) != 0:
            flow.reply(
                text=f"new users Added: \n{list_users}"
            )

    elif flow.token.startswith('get_event_specific'):
        res = flow.response

        event_type = modules.EventType[res["event_type"]]

        # TODO get event specific

        # if res["date"] ==
        # date = datetime.date.fromtimestamp(int(res["date"]) / 1000)
        #
        # get_event = repository.get_event(
        #     wa_id=wa_id,
        #     type_event=event_type,
        #     date=date
        # )
        # print(get_event.type)

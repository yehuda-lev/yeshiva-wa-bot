import re

from db import repository


def get_data_source(index: int, list_users: list) -> list[dict]:
    data_source = []

    for user in list_users[index: (index + 20)]:
        data_source.append(
            user
        )
    if len(data_source) == 0:
        data_source.append({"id": "0"})
    return data_source


def get_data_users(filter_pay: bool = None, filter_in_program: bool = None) -> dict:

    # get all users
    all_users = [
        {
            "id": k,
            "title": v[0],
            "description": re.sub("^972", "0", k)}
        for k, v in repository.get_all_users(pay=filter_pay, in_program=filter_in_program).items()
    ]

    # handle the dict
    (is_group_1_visible, is_group_2_visible,
     is_group_3_visible, is_group_4_visible) = False, False, False, False

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

    return {
        "data_people_group_1": people_group_1,
        "data_is_group_1_visible": is_group_1_visible,
        "data_people_group_2": people_group_2,
        "data_is_group_2_visible": is_group_2_visible,
        "data_people_group_3": people_group_3,
        "data_is_group_3_visible": is_group_3_visible,
        "data_people_group_4": people_group_4,
        "data_is_group_4_visible": is_group_4_visible
    }
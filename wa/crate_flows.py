from pywa import WhatsApp, types, utils, errors
from pywa.types import flows
from pprint import pprint

from data.utils import get_settings
from data import modules


settings = get_settings()

wa = WhatsApp(
    phone_id=settings.WA_PHONE_ID,
    token=settings.WA_TOKEN,
    business_account_id=settings.WA_BUSINESS_ID,
)

#  create_flow
# create_flow = wa.create_flow(
#     name='managing_dates_events_and_users',
#     categories=[types.FlowCategory.CUSTOMER_SUPPORT],
# )  # -> 774420634511632

flow_id = 774420634511632
print(flow_id)
# pprint(wa.get_flow(flow_id=flow_id))


managing_dates_events_and_users = types.FlowJSON(
    version=utils.Version.FLOW_JSON,
    data_api_version=utils.Version.FLOW_DATA_API,
    routing_model={
        "choose_date_and_type": ["choose_people"],
        "user_details": ["choose_people"],
    },
    screens=[
        flows.Screen(
            id='choose_date_and_type',
            title='בחירת תאריך וסוג האירוע',
            terminal=False,
            data=[
                welcome_user := flows.ScreenData(key="welcome_user", example="hello john"),
                is_event_type_required := flows.ScreenData(key="is_event_type_required", example=True),
                # default_date := flows.ScreenData(key="default_date", example="1704118927")
            ],
            layout=flows.Layout(
                type=flows.LayoutType.SINGLE_COLUMN,
                children=[
                    flows.Form(
                        name='Form',
                        children=[
                            flows.TextHeading(text=welcome_user.data_key),

                            flows.TextBody(text='נא לבחור את סוג הלימוד'),
                            event_type := flows.RadioButtonsGroup(
                                name='event_type',
                                label='סוג הלימוד',
                                data_source=[
                                    flows.DataSource(
                                        id=modules.EventType.SHACHRIS.name,
                                        title='שחרית'
                                    ),
                                    flows.DataSource(
                                        id=modules.EventType.SEDER_ALEF.name,
                                        title='סדר א'
                                    ),
                                    flows.DataSource(
                                        id=modules.EventType.SEDER_BET.name,
                                        title='סדר ב'
                                    ),
                                    flows.DataSource(
                                        id=modules.EventType.SEDER_GIMEL.name,
                                        title='סדר ג'
                                    ),
                                ],
                                required=is_event_type_required.data_key,
                            ),

                            flows.TextBody(text='נא לבחור את התאריך'),
                            date := flows.DatePicker(
                                name='date',
                                label='תאריך',
                                # init_value=default_date.data_key,
                                # init_value=str(datetime.datetime.today().timestamp()),
                                required=True,
                            ),

                            flows.Footer(
                                label='המשך',
                                on_click_action=flows.Action(
                                    name=flows.FlowActionType.DATA_EXCHANGE,
                                    payload={
                                        "event_type": event_type.form_ref,
                                        "date": date.form_ref,
                                    }
                                ),
                            ),
                        ],

                    )
                ]
            ),
        ),

        flows.Screen(
            id='choose_people',
            title='בחירת בחורים',
            terminal=True,
            data=[
                data_type_get_user := flows.ScreenData(key="type_get_user", example=["get_info"]),
                data_get_user := flows.ScreenData(key="get_user", example="12"),
                event_type := flows.ScreenData(key="event_type", example="shachris"),
                date := flows.ScreenData(key="date", example="30/12/32023"),

                data_people_group_1 := flows.ScreenData(
                    key="data_people_group_1",
                    example=[flows.DataSource(id="972", title="Yehuda", description="972")]
                ),
                data_is_group_1_visible := flows.ScreenData(key="data_is_group_1_visible", example=True),

                data_people_group_2 := flows.ScreenData(
                    key="data_people_group_2",
                    example=[flows.DataSource(id="972", title="Yehuda", description="972")]
                ),
                data_is_group_2_visible := flows.ScreenData(key="data_is_group_2_visible", example=True),

                data_people_group_3 := flows.ScreenData(
                    key="data_people_group_3",
                    example=[flows.DataSource(id="972", title="Yehuda", description="972")]
                ),
                data_is_group_3_visible := flows.ScreenData(key="data_is_group_3_visible", example=True),

                data_people_group_4 := flows.ScreenData(
                    key="data_people_group_4",
                    example=[flows.DataSource(id="972", title="Yehuda", description="972")]
                ),
                data_is_group_4_visible := flows.ScreenData(key="data_is_group_4_visible", example=True),
            ],
            layout=flows.Layout(
                type=flows.LayoutType.SINGLE_COLUMN,
                children=[
                    flows.Form(
                        name='form',
                        children=[
                            flows.TextBody(text='נא לבחור את המשתמשים'),
                            people_group_1 := flows.CheckboxGroup(
                                name="people_group_1",
                                data_source=data_people_group_1.data_key,
                                visible=data_is_group_1_visible.data_key,
                            ),
                            people_group_2 := flows.CheckboxGroup(
                                name="people_group_2",
                                data_source=data_people_group_2.data_key,
                                visible=data_is_group_2_visible.data_key,
                            ),
                            people_group_3 := flows.CheckboxGroup(
                                name="people_group_3",
                                data_source=data_people_group_3.data_key,
                                visible=data_is_group_3_visible.data_key,
                            ),
                            people_group_4 := flows.CheckboxGroup(
                                name="people_group_4",
                                data_source=data_people_group_4.data_key,
                                visible=data_is_group_4_visible.data_key,
                            ),
                            flows.Footer(
                                label='סיום',
                                on_click_action=flows.Action(
                                    name=flows.FlowActionType.COMPLETE,
                                    payload={
                                        "event_type": event_type.data_key,
                                        "date": date.data_key,
                                        "people_group_1": people_group_1.form_ref,
                                        "people_group_2": people_group_2.form_ref,
                                        "people_group_3": people_group_3.form_ref,
                                        "people_group_4": people_group_4.form_ref,

                                        "data_type_get_user": data_type_get_user.data_key,
                                        "data_get_user": data_get_user.data_key,
                                    }
                                ),
                            )
                        ],
                    )
                ]
            ),
        ),

        flows.Screen(
            id='user_details',
            title='עריכת פרטי המשתמש',
            terminal=True,
            data=[
                data_ask_user_details := flows.ScreenData(
                    key="data_ask_user_details",
                    example=[flows.DataSource(id="972", title="Yehuda")]
                ),
            ],
            layout=flows.Layout(
                type=flows.LayoutType.SINGLE_COLUMN,
                children=[
                    flows.Form(
                        name='form',
                        children=[
                            get_user := flows.Dropdown(
                                name="ניהול משתמשים",
                                label="בחר את סוג המידע",
                                required=True,
                                data_source=data_ask_user_details.data_key,
                            ),

                            type_get_user := flows.CheckboxGroup(
                                name='מה ברצונך לעשות',
                                max_selected_items=1,
                                required=True,
                                data_source=[
                                    flows.DataSource(
                                        id="get_info",
                                        title="קבלת פרטים",
                                        description="קבלת פרטים על משתמשים.\n"
                                                    "לדוגמה, קבלת כל המשתמשים שמשתתפים במבצע"
                                    ),
                                    flows.DataSource(
                                        id="edit_info",
                                        title="שינוי פרטים",
                                        description="עריכת פרטים של משתמשים.\n"
                                                    "לדוגמה, שינוי משתמשים שלא במבצע והגדרתם למשתתפים במבצע"
                                    ),
                                ]
                            ),

                            flows.Footer(
                                label='המשך',
                                on_click_action=flows.Action(
                                    name=flows.FlowActionType.DATA_EXCHANGE,
                                    payload={
                                        "get_user": get_user.form_ref,
                                        "type_get_user": type_get_user.form_ref,
                                    }
                                ),
                            )
                        ],
                    )
                ]
            ),
        )
    ]
)

# print(json.dumps(customer_satisfaction_survey.to_dict()))
# pprint(managing_dates_events_and_users)

# try:
#     edit_flow = wa.update_flow_json(flow_id=flow_id, flow_json=managing_dates_events_and_users)
#     pprint(edit_flow)
# except errors.FlowUpdatingError:
#     print("Error updating flow")
#     pprint(wa.get_flow(flow_id=flow_id).validation_errors)

# update_flow_metadate = wa.update_flow_metadata(
#     flow_id=flow_id,
#     endpoint_uri=f'{settings.CALLBACK_URL}/support_request_flow')
# print(update_flow_metadate)

pprint(wa.get_flow(flow_id=flow_id))
pprint(wa.get_flow_assets(flow_id))

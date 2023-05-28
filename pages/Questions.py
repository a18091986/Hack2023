import random
import pickle as pkl
import dash
import numpy as np
import pandas as pd
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import tensorflow as tf

from dash_elements import generate_carousel
from df_prepare import get_dist
from pages.TABS.exist_user_tab import generate_exist_user_tab_content
from pages.TABS.new_user_tab import generate_new_user_tab_content
from pages.model import model, index
from usefull_func import get_coords

df_recs = pd.read_csv('datasets_prep/recs_data_names.csv')
df_groups = pd.read_csv('datasets_prep/groups_with_coords.csv')
dict_df = pd.read_csv('datasets_prep/dict.csv')
df_users = pd.read_csv('datasets_prep/users_with_coords.csv')

df_recs['start_age'] = df_recs['age_group'].apply(lambda x: int(x.split('-')[0]))
df_recs['stop_age'] = df_recs['age_group'].apply(lambda x: int(x.split('-')[1]))

with open('serialize/top_recs.pkl', 'rb') as f:
    top_recs = pkl.load(f)
    # print(top_recs)

dash.register_page(__name__, path='/Questions', name='recommend')

layout = html.Div([
    html.Div([dbc.Alert([
        html.H4('Questions'),
    ], color="primary")]),
    dcc.Tabs(
        id='tabs_questions',
        value='tabs_questions',
        children=[dcc.Tab(label='Новый пользователь', value='new_user_tab'),
                  dcc.Tab(label='Существующий пользователь', value='exist_user_tab'),
                  ]),
    html.Div(id='tabs_content_questions', children=generate_new_user_tab_content()),
])


@callback(Output('tabs_content_questions', 'children'),
          Input('tabs_questions', 'value'),
          prevent_initial_call=True)
def render_tabs_body(tab):
    print(model, index)
    if tab == 'new_user_tab':
        return generate_new_user_tab_content()
    elif tab == 'exist_user_tab':
        return generate_exist_user_tab_content()
    else:
        return "404"


@callback(Output(component_id="carousel_wrapper", component_property='children', allow_duplicate=True),
          Output(component_id="get_group_by_line3_exist_user_wrapper", component_property='children'),
          Input('get_recs_exist_user_btn', 'n_clicks'),
          State('id_input', 'value'),
          prevent_initial_call=True)
def get_recs_exist_users(n, idx):
    _, titles = index(np.array([str(idx)]))
    recs = [[dict_df[dict_df.id_level3 == int(tf.squeeze(title).numpy().decode('utf-8'))]['line_3'].values[0]]
            for title in titles[0]]
    return generate_carousel(recs), dbc.Button("Show groups", color="info", id='get_group_by_line3_exist_user_btn')


@callback(Output(component_id="group_select_exist_user_wrapper", component_property='children'),
          Input('get_group_by_line3_exist_user_btn', 'n_clicks'),
          State('recomenadations_carousel', 'items'),
          State('recomenadations_carousel', 'active_index'),
          State('id_input', 'value'),
          prevent_initial_callback=True)
def get_recs_groups_exist_users(n, items, item_idx, user_idx):
    item_idx = item_idx if item_idx else 0
    line_3 = items[item_idx].get('header')[0]
    #
    # print(user_idx)
    # print(items)
    # print(item_idx)
    # print(line_3)
    #
    # return ''
#
    active_groups = df_groups[(df_groups['направление 3'] == line_3)
                              & (df_groups['расписание в плановом периоде']
                                 .notna())][['уникальный номер',
                                             'направление 3',
                                             'район площадки',
                                             'адрес площадки',
                                             'расписание в плановом периоде',
                                             'latitude',
                                             'longitude'
                                             ]] \
        .to_numpy().tolist()

    print(active_groups)
    user_coords = df_users[df_users['уникальный номер'] == user_idx][['latitude', 'longitude']].to_numpy().tolist()[0]
    print(user_coords)
    if active_groups:
        cards = [dbc.Col(dbc.Card(
            [
                dbc.CardHeader(f"ID: {group[0]}"),
                dbc.CardBody(
                    [
                        html.H5(f"{group[1]}", className="card-title"),
                        html.P(f"{(group[2].split(',')[1] if len(group[2].split(',')) > 1 else group[2]) if group[2] else ''}",
                               className="card-text"),
                        html.P(f"{group[4]}", className="card-text"),
                    ]),
                dbc.CardFooter(f"Примерное расстояние: "
                               f"{int(get_dist(user_coords[0], user_coords[1], group[5], group[6]))} км"
                               if user_coords and group[5] and group[6] else ''),
                dbc.Button("Записаться", color="primary")],
            style={"width": "18rem", 'min-height': '500px', 'margin': "5"}), width=4, align="center") for group in
            active_groups]
        if user_coords:
            cards = sorted(cards,
                           key=lambda x: int(x.children.children[-2].children.split(':')[1].split('км')[0].strip()))
        return cards
    else:
        card = dbc.Card(
            [
                dbc.CardHeader(f"ID: "),
                dbc.CardBody(
                    [
                        html.H5(f"{line_3}", className="card-title"),
                        html.P(f"В настоящее время не проводится групп по выбранному Вами направлению",
                               className="card-text"),
                        html.P(f"Вы можете оставить заявку на организацию такой группы", className="card-text"),
                    ]),
                dbc.Button("Хочу группу!", color="primary")],
            style={"width": "18rem", 'min-height': '500px', 'margin': "5"})
        return card


@callback(
    Output(component_id="carousel_wrapper", component_property='children'),
    Output(component_id="city_input_wrapper", component_property='children'),
    Output(component_id="street_input_wrapper", component_property='children'),
    Output(component_id="get_group_by_line3_new_user_wrapper", component_property='children'),

    Input(component_id="get_recs_new_user_btn", component_property='n_clicks'),
    State(component_id='dropdown_gender', component_property='value'),
    State(component_id='fio_input', component_property='value'),
    State(component_id='age_input', component_property='value'),
    prevent_initial_call=True)
def get_recommendations_gender_age(n, gender, fio, age):
    top_recs = df_recs[(df_recs.gender == gender) &
                       (df_recs['start_age'] <= age) &
                       (age < df_recs['stop_age'])]['recs'].values[0]
    print(top_recs)
    return \
        generate_carousel(eval(top_recs)), \
        dbc.Input(placeholder='Город', id='city_input'), \
        dbc.Input(placeholder='Улица', id='street_input'), \
        dbc.Button("Show groups", color="info", id='get_group_by_line3_new_user_btn')


@callback(Output(component_id="group_select_new_user_wrapper", component_property='children'),
          Output(component_id="city_input_wrapper", component_property='children', allow_duplicate=True),
          Output(component_id="street_input_wrapper", component_property='children', allow_duplicate=True),
          State('recomenadations_carousel', 'items'),
          State('city_input', 'value'),
          State('street_input', 'value'),
          State('recomenadations_carousel', 'active_index'),
          Input('get_group_by_line3_new_user_btn', 'n_clicks'),
          prevent_initial_call=True)
def get_recs_new_users(items, city, street, idx, n):
    idx = idx if idx else 0
    line_3 = items[idx].get('header')
    active_groups = df_groups[(df_groups['направление 3'] == line_3)
                              & (df_groups['расписание в плановом периоде']
                                 .notna())][['уникальный номер',
                                             'направление 3',
                                             'район площадки',
                                             'адрес площадки',
                                             'расписание в плановом периоде',
                                             'latitude',
                                             'longitude'
                                             ]] \
        .to_numpy().tolist()
    user_coords = None
    if city and street:
        city = city.replace('город', '').replace('г.', '').replace('.', '').replace('Г.', '')
        user_coords = get_coords(city, street)
    if active_groups:
        cards = [dbc.Col(dbc.Card(
            [
                dbc.CardHeader(f"ID: {group[0]}"),
                dbc.CardBody(
                    [
                        html.H5(f"{group[1]}", className="card-title"),
                        html.P(f"{group[2].split(',')[1] if len(group[2].split(',')) > 1 else group[2]}",
                               className="card-text"),
                        html.P(f"{group[4]}", className="card-text"),
                    ]),
                dbc.CardFooter(f"Примерное расстояние: "
                               f"{int(get_dist(user_coords[0], user_coords[1], group[5], group[6]))} км"
                               if user_coords else
                               "Введите Ваш адрес, чтобы отсортировать группы по удаленности"),
                dbc.Button("Записаться", color="primary")],
            style={"width": "18rem", 'min-height': '500px', 'margin': "5"}), width=4, align="center") for group in
            active_groups]
        if user_coords:
            cards = sorted(cards,
                           key=lambda x: int(x.children.children[-2].children.split(':')[1].split('км')[0].strip()))
        return (cards,
                dbc.Input(placeholder='Город', id='city_input'),
                dbc.Input(placeholder='Улица', id='street_input'))
    else:
        card = dbc.Card(
            [
                dbc.CardHeader(f"ID: "),
                dbc.CardBody(
                    [
                        html.H5(f"{line_3}", className="card-title"),
                        html.P(f"В настоящее время не проводится групп по выбранному Вами направлению",
                               className="card-text"),
                        html.P(f"Вы можете оставить заявку на организацию такой группы", className="card-text"),
                    ]),
                dbc.Button("Хочу группу!", color="primary")],
            style={"width": "18rem", 'min-height': '500px', 'margin': "5"})
        return (card,
                dbc.Input(placeholder='Город', id='city_input'),
                dbc.Input(placeholder='Улица', id='street_input'))

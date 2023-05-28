import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc


from pages.TABS.groups import generate_group_tab_content
from pages.TABS.users import generate_user_tab_content
from pages.TABS.attend import generate_attend_tab_content
from pages.model import model, index

dash.register_page(__name__, path='/', name='EDA')

# for chunk in pd.read_csv('datasets_prep/result_df_with_dist.csv', chunksize=1000000):
#     chunk['u_g_dist'] = chunk['u_g_dist'].astype('int')
#     result = chunk
#     break

users = pd.read_csv('datasets_prep/users.csv')
groups_with_coords = pd.read_csv('datasets_prep/groups_with_coords.csv')
users_with_coords = pd.read_csv('datasets_prep/users_with_coords.csv')
dict_df = pd.read_csv('datasets_prep/dict.csv')


layout = html.Div([
    html.Div([dbc.Alert([
        html.H4('EDA'),
        html.Hr(),
    ], color="primary")]),
    dcc.Tabs(
        id='tabs_eda',
        value='tabs_eda',
        children=[dcc.Tab(label='Users', value='users_tab'),
                  dcc.Tab(label='Groups', value='groups_tab'),
                  dcc.Tab(label='Attend', value='attend_tab'),
                  ]),
    html.Div(id='tabs-content', children=generate_user_tab_content(users)),

])


@callback(Output('tabs-content', 'children'),
          Input('tabs_eda', 'value'),
          prevent_initial_call=True)
def render_tabs_body(tab):
    if tab == 'users_tab':
        return generate_user_tab_content(users)
    elif tab == 'groups_tab':
        return generate_group_tab_content(groups_with_coords, dict_df)
    elif tab == 'attend_tab':
        return generate_attend_tab_content()
    else:
        return "404"

from dash import html
import dash_bootstrap_components as dbc
import pickle as pkl

from dash_elements import generate_carousel, generate_dropdown_gender

with open('serialize/top_recs.pkl', 'rb') as f:
    top_recs = pkl.load(f)


def generate_new_user_tab_content():
    layout = html.Div([
        html.P(),
        html.Div(dbc.Input(placeholder='Фамилия Имя Отчество', id='fio_input'), className="mb-3",
                 id='fio_input_wrapper'),
        html.Div(generate_dropdown_gender(), id='dropdown_gender_wrapper'),
        html.P(),
        html.Div(dbc.Input(placeholder='Возраст', id='age_input', type='number'), className='mb-3',
                 id='age_input_wrapper'),
        html.P(),
        html.Div(dbc.Button("Get recommendations", color="info", id='get_recs_new_user_btn'),
                 className="d-grid gap-2 col-6 mx-auto"),
        html.P(),
        html.Div([dbc.Alert([
            html.H4('Recommendations'),
        ], color="success")]),
        html.Div(generate_carousel(top_recs), id='carousel_wrapper'),
        html.P(),
        html.Div(dbc.Input(placeholder='Город', id='city_input', type='hidden'), className='mb-3', id='city_input_wrapper'),
        html.Div(dbc.Input(placeholder='Улица', id='street_input', type='hidden'), className='mb-3', id='street_input_wrapper'),
        html.P(),
        html.Div(dbc.Button("Show groups", color="info", id='get_group_by_line3_new_user_btn'),
                 className="d-grid gap-2 col-6 mx-auto", id='get_group_by_line3_new_user_wrapper'),
        html.P(),
        dbc.Row(id='group_select_new_user_wrapper', align="center", justify="center"),
        html.P()
    ])
    return layout

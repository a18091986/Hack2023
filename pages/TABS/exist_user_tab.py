from dash import html
import dash_bootstrap_components as dbc
import pickle as pkl

with open('serialize/top_recs.pkl', 'rb') as f:
    top_recs = pkl.load(f)


def generate_exist_user_tab_content():
    layout = html.Div([
        html.P(),
        html.Div(dbc.Input(placeholder='Фамилия Имя Отчество (поле ввода отключено ввиду отсутсвия в датасете данных)',
                           id='fio_input', disabled=True), className="mb-3",
                 id='fio_input_wrapper'),
        html.Div(dbc.Input(placeholder='ID', id='id_input', type='number'), className='mb-3', id='age_input_wrapper'),
        html.Div(dbc.Button("Get recommendations", color="info", id='get_recs_exist_user_btn'), className="d-grid gap-2 col-6 mx-auto"),
        html.P(),
        html.Div([dbc.Alert([
            html.H4('Recommendations'),

        ], color="success")]),
        html.P(),
        html.Div(id='carousel_wrapper'),
        html.P(),
        html.Div(className="d-grid gap-2 col-6 mx-auto", id='get_group_by_line3_exist_user_wrapper'),
        html.P(),
        dbc.Row(id='group_select_exist_user_wrapper', align="center", justify="center"),
        html.P()
    ])

    return layout

import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import math
import folium
import io
from PIL import Image


def generate_user_tab_content(users: pd.DataFrame):
    histogram_gender = px.histogram(users, x='gender', histnorm='percent', text_auto=True)
    histogram_gender['layout'].update(title=dict(
        text='Процентное соотношение <br> женщин и мужчин в датасете',
        x=0.5,
        y=0.95
    ),
        template='ggplot2',
        font=dict(size=16),
        xaxis_title='Пол', yaxis_title='%')

    histogram_age_female = px.histogram(users[users.gender == 'Женщина'], x='age')
    histogram_age_female['layout'].update(title=dict(text='Распределение женщин по возрасту',
                                                     x=0.5,
                                                     y=0.95),
                                          template='ggplot2',
                                          font=dict(size=16),
                                          xaxis_title='возраст', yaxis_title='количество пользователей')

    histogram_age_male = px.histogram(users[users.gender == 'Мужчина'], x='age')
    histogram_age_male['layout'].update(title=dict(text='Распределение мужчин по возрасту',
                                                   x=0.5,
                                                   y=0.95),
                                        template='ggplot2',
                                        font=dict(size=16),
                                        xaxis_title='возраст', yaxis_title='количество пользователей')

    # histogram_dist_u_g = px.histogram(result[(result.online_offline == 'Нет')
    #                                          & (result.u_g_dist < 20)], x='u_g_dist')
    # histogram_dist_u_g['layout'].update(title=dict(text='Распределение расстояний пользователь-группа',
    #                                                x=0.5,
    #                                                y=0.95),
    #                                     template='ggplot2',
    #                                     font=dict(size=16),
    #                                     xaxis_title='расстояние, км', yaxis_title='количество пользователей')

    # mapit = folium.Map(location=[0, 0], zoom_start=1)
    #
    # for lat, lon in zip(users_with_coords[:5000].latitude, users_with_coords[:5000].longitude):
    #     if not math.isnan(lat) and not math.isnan(lon):
    #         folium.Marker(location=[lat, lon], fill_color='#43d9de', radius=8).add_to(mapit)
    #
    # mapit.save('test.html')
    # img_data = mapit._to_png(5)
    # img = Image.open(io.BytesIO(img_data))
    # img.save('image.png')

    body = [
        html.Div(dcc.Graph(figure=histogram_gender)),
        dbc.Row([dbc.Col(dcc.Graph(figure=histogram_age_male)), dbc.Col(dcc.Graph(figure=histogram_age_female))]),
        # html.Div(dcc.Graph(figure=histogram_dist_u_g)),
        html.Div(html.Img(src='static/images/user_group_distance.PNG'), style={'margin-left': '40px', 'margin-bottom': '50px'}),
        html.H4("Произведено геокодирование адресов пользователей"),
        html.Div(html.Img(src='static/images/users_geo.PNG'), style={'margin-left': '40px', 'margin-bottom': '50px'})
    ]

    return body

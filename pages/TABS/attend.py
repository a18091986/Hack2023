import plotly.express as px
import pandas as pd
from dash import dcc, html

import dash_bootstrap_components as dbc
import math
import folium
import io
from PIL import Image


def generate_attend_tab_content():
    # histogram_online_offline_attend = px.histogram(result[['online_offline', 'gender']],
    #                                                x='online_offline',
    #                                                color='gender',
    #                                                text_auto=True,
    #                                                height=700)
    # histogram_online_offline_attend['layout'].update(title=dict(text='Предпочтения пользователей online/offline',
    #                                                             x=0.5,
    #                                                             y=0.95),
    #                                                  template='ggplot2',
    #                                                  font=dict(size=16),
    #                                                  xaxis_labelalias={'Да': 'Онлайн', 'Нет': 'Оффлайн'},
    #                                                  xaxis_title='', yaxis_title='количество пользователей')

    # histogram_female_count_attend = px.histogram(result['user_id'][result['gender'] == 'Женщина']
    #                                              .value_counts(),
    #                                              x='count',
    #                                              height=500,
    #                                              nbins=50)
    # histogram_female_count_attend['layout'].update(title=dict(text='Количество посещений занятий женщинами',
    #                                                           x=0.5,
    #                                                           y=0.95),
    #                                                template='ggplot2',
    #                                                font=dict(size=16),
    #                                                # xaxis_labelalias={'Да': 'Онлайн', 'Нет': 'Оффлайн'},
    #                                                xaxis_title='', yaxis_title='количество пользователей')
    #
    # histogram_male_count_attend = px.histogram(result['user_id'][result['gender'] == 'Мужчина']
    #                                            .value_counts(),
    #                                            x='count',
    #                                            height=500,
    #                                            nbins=50)
    # histogram_male_count_attend['layout'].update(title=dict(text='Количество посещений занятий мужчинами',
    #                                                         x=0.5,
    #                                                         y=0.95),
    #                                              template='ggplot2',
    #                                              font=dict(size=16),
    #                                              # xaxis_labelalias={'Да': 'Онлайн', 'Нет': 'Оффлайн'},
    #                                              xaxis_title='', yaxis_title='количество пользователей')
    #
    # result['online'] = result['online_offline'].apply(lambda x: 'онлайн' if "Да" in x else 'оффлайн')
    # histogram_attend_type = px.histogram(result[['markup', 'online']], x='markup', color='online',
    #                                      text_auto=True)
    # histogram_attend_type['layout'].update(title=
    #                                        dict(text='Распределение посещений групп по направлениям: душа, тело, мозг',
    #                                             x=0.5,
    #                                             y=0.95),
    #                                        template='ggplot2',
    #                                        font=dict(size=16),
    #                                        xaxis_title='направление', yaxis_title='количество')
    #
    body = [
        html.Div(html.Img(src='static/images/attend_online_offline_count.PNG'), style={'margin-left': '40px',
                                                                                       'margin-bottom': '50px',
                                                                                       'margin-top': '50px'}),
        html.Div(html.Img(src='static/images/attend_count_female.PNG'), style={'margin-left': '40px',
                                                                                       'margin-bottom': '50px',
                                                                                       'margin-top': '50px'}),
        html.Div(html.Img(src='static/images/attend_count_male.PNG'), style={'margin-left': '40px',
                                                                                       'margin-bottom': '50px',
                                                                                       'margin-top': '50px'}),
        html.Div(html.Img(src='static/images/attend_direction_type.PNG'), style={'margin-left': '40px',
                                                                                       'margin-bottom': '50px',
                                                                                       'margin-top': '50px'}),

        # html.Div(dcc.Graph(figure=histogram_online_offline_attend)),
        # html.Div(dcc.Graph(figure=histogram_female_count_attend)),
        # html.Div(dcc.Graph(figure=histogram_male_count_attend)),
        # html.Div(dcc.Graph(figure=histogram_attend_type)),
    ]

    return body

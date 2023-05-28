import plotly.express as px
import pandas as pd
from dash import dcc, html


def generate_group_tab_content(groups: pd.DataFrame, dict_df: pd.DataFrame):
    groups['направление 1'] = groups['направление 1'] \
        .apply(lambda x: x.replace('(спецпроект по медицинской реабилитации)', ''))
    histogram_level1 = px.histogram(groups, x='направление 1',
                                    histnorm='percent', height=700, text_auto=True, )
    histogram_level1['layout'].update(title=dict(text='Распределение групп по направлениям',
                                                 x=0.5,
                                                 y=0.95
                                                 ),
                                      template='ggplot2',
                                      font=dict(size=16),
                                      xaxis_title='Направление занятий', yaxis_title='%')

    dict_df['online'] = dict_df['line_3'].apply(lambda x: 'онлайн' if "ОНЛАЙН" in x else 'оффлайн')
    histogram_group_type = px.histogram(dict_df[['markup', 'online']], x='markup', color='online',
                                        text_auto=True)
    histogram_group_type['layout'].update(title=dict(text='Распределение групп по направлениям: душа, тело, мозг',
                                                     x=0.5,
                                                     y=0.95),
                                          template='ggplot2',
                                          font=dict(size=16),
                                          xaxis_title='направление', yaxis_title='количество')

    body = [
        html.Div(dcc.Graph(figure=histogram_level1)),
        html.Div(dcc.Graph(figure=histogram_group_type)),
        html.H4("Произведено геокодирование адресов проведения групп"),
        html.Div(html.Img(src='static/images/groups_geo.PNG'), style={'margin-left': '150px', 'margin-bottom': '50px'})
    ]

    return body

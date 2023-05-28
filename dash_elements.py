import dash_bootstrap_components as dbc
from dash import dcc, html

def generate_dropdown_gender():
    return dcc.Dropdown([answer for n, answer in enumerate(["Мужчина", "Женщина"])],
                        id="dropdown_gender",
                        className='center_elements',
                        placeholder="Пол",
                        optionHeight=30,
                        style={'height': '50px',
                               'font-size': '20px'})


def generate_carousel(recs):
    slide_path = "/static/images/slide.jpg"
    return dbc.Carousel(
        items=[dict(key=i, src=slide_path, header=rec,  # caption=rec[0],
                    img_style={"height": "200px"})
               for i, rec in enumerate(recs)],
        variant="dark",
        id='recomenadations_carousel')

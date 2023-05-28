from recommendations_DSSM import DSSM_model
import dash
from dash import html

index, model = DSSM_model()
dash.register_page(__name__, path='/model', name='model')
layout = html.Div([])
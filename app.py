import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True, use_pages=True)

app.config.suppress_callback_exceptions = True


sidebar = dbc.Nav(
    [dbc.NavLink([html.Div(page['name'], className='ms-2')], href=page['path'], active='exact',
                 style={"margin": "10px 10px 10px 10px"})
     for page in dash.page_registry.values()][:-1],
    vertical=True,
    pills=True,
    className="bg-light"
)

body = dbc.Container([
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ])
], fluid=False)

app.layout = body

if __name__ == '__main__':
    app.run_server(port=1919, host='192.168.2.33')

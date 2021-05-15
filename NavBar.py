import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import date


def get_current_date():
    return date.today().strftime("%d/%m/%Y")


def navgationbar():
    # css to overwrite the initial css.
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 70,
        "left": 0,
        "bottom": 0,
        "width": "14rem",
        "padding": "2rem 1rem",
        "background-color": "#F3F3F3",
        'color': '#484848',
        'border-top': 'thin solid #EEFBFB',
        'border-right': 'thin solid #EEFBFB',
        'box-shadow': '0 0px 1px 0px'
    }

    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
        'color': '#484848'
    }

    sidebar = html.Div(
        [
            html.H2("Menu",
                    className="display-5"),
            html.Hr(),
            html.P(
                "Navigation menu for the app",
                className="lead"
            ),
            html.P(f'The date is: {get_current_date()}'),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Analyze", href="/page-1", active="exact"),
                    dbc.NavLink("Prediction", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content",
                       children=[],
                       style=CONTENT_STYLE)

    return sidebar, content

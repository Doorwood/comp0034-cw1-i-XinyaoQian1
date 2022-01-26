"""
# @File    :    navbar_example.py
# @Time    :    22/01/2022 23:03
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Output, Input, State

PLOTLY_LOGO = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
external_stylesheets = [dbc.themes.BOOTSTRAP, ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                # make it responsive to mobile
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Seoul Bike Company",
                                                className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavLink("Internal link1", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link2", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link3", href="/l/components/nav",
                        active=True),
            dbc.NavLink("Internal link4", href="/l/components/nav",
                        active=True),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),

        ]
    ),
    color="dark",
    dark=True,
)
row1 = dbc.Row([  # row1
    dbc.Col('Column 1', width=6),
    dbc.Col('Column 2', width=3),
    dbc.Col('Column 3', width=3),
    html.Div(children='hello'),

])
row2 = dbc.Row([  # row2
    dbc.Col('Column 1', width=5),
    dbc.Col('Column 2', width=4),
    dbc.Col('Column 3', width=3),
])
app.layout = dbc.Container([
    navbar,
    row1,
    row2,

])


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)

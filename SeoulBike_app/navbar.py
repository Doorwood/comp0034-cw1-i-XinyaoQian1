"""
# @File    :    navbar.py
# @Time    :    03/02/2022 10:38
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: 
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def nav_bar():
    PLOTLY_LOGO = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
    # Search bar
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
                dbc.NavLink("View Profile", href="/l/components/nav",
                            active=True),
                dbc.NavLink("Dashboards", href="/l/components/nav",
                            active=True),
                dbc.NavLink("Reports", href="/l/components/nav",
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
        color="grey",
        dark=True,
    )
    return navbar

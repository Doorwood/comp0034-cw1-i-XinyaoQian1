"""
# @File    :    seoul_bike_elements.py
# @Time    :    03/02/2022 10:38
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description: Elements in dash app.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def nav_bar():
    """

    Returns: navigation bar of the dash app

    """
    logo = "https://s2.loli.net/2022/01/21/bl8ZS5vzwjA3YaM.png"
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
                    # Use row and col to control vertical alignment of logo /
                    # brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=logo, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Seoul Bike Company",
                                                    className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="http://127.0.0.1:5050",
                    style={"textDecoration": "none"},
                ),
                dbc.NavLink("Back to Home", href="http://127.0.0.1:5050/",
                            active=True),
                # dbc.NavLink("Dashboards", href="/l/components/nav",
                #             active=True),
                # dbc.NavLink("Reports", href="/l/components/nav",
                #             active=True),

                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

                # dbc.Collapse(
                #     search_bar,
                #     id="navbar-collapse",
                #     is_open=False,
                #     navbar=True,
                # ),

            ]
        ),
        color="dark",

        dark=True,
    )
    return navbar


def dropdown():
    """

    Returns:
        card-body containing two dropdowns

    """
    month_name = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July',
                  'August', 'September', 'October', 'November', 'December']
    month_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # Adapted from Online Course: Learn Bootstrap
    # https://www.codecademy.com/learn/learn-bootstrap
    drp = [dbc.CardBody([
        html.H6('Select Months', style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col([
                html.H6('Current Month'),
                dcc.Dropdown(id='dropdown_base',
                             options=[
                                 {'label': i, 'value': j} for (i, j) in
                                 zip(month_name, month_number)
                             ],
                             value=1,
                             )
            ]),
            dbc.Col([
                html.H6('Reference Month'),
                dcc.Dropdown(id='dropdown_comp',
                             options=[
                                 {'label': i, 'value': j} for (i, j) in
                                 zip(month_name, month_number)
                             ],
                             value=1,
                             )
            ]),

        ])

    ])]
    return drp


def card_text(title, text, subtext=None):
    """

    Args:
        title (str): title of the card body
        text (Object): main text on the card
        subtext (Object): subtext on the card

    Returns:
        card-body containing title, text and subtext

    """
    new_card = [dbc.CardBody(
        [
            html.H6(title,
                    style={'fontWeight': 'lighter', 'textAlign': 'center'}),

            html.H3(f'{text}',
                    style={'color': '#090059', 'textAlign': 'center'}),

            subtext

        ]

    )]
    return new_card


def card_double_figure(title, fig1, fig2, height='400px'):
    """
    Args:
        title (str): title of the card body
        fig1 (figure): first figure
        fig2 (figure): second figure
        height (str): height of the figures

    Returns:
        card-body containing title, fig1 and fig2

    """
    new_card = [

        dbc.CardBody(
            [
                html.H6(title,
                        style={'fontWeight': 'lighter', 'textAlign': 'center'}),

                dbc.Row([
                    dbc.Col([dcc.Graph(figure=fig1,
                                       style={'height': height}),
                             ]),
                    dbc.Col([dcc.Graph(figure=fig2,
                                       style={'height': height}),
                             ])

                ])

            ]

        )
    ]
    return new_card


def card(title, figure, height='390px', width='390px'):
    """

    Args:
        title (str): title of the card
        figure (figure): figure included in the card
        height (str): height of the figure
        width (str): width of the figure

    Returns:
        card-body containing given parameters

    """
    new_card = [dbc.Card(
        dbc.CardBody(
            [html.H6(title,
                     style={'fontWeight': 'lighter', 'textAlign': 'center'}),
             dcc.Graph(figure=figure,
                       style={'height': height, 'width': width})
             ]

        ))
    ]
    return new_card

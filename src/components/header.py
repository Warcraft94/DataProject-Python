from dash import html, dcc

def create_header(years):
    return html.Header(
        id="header",
        children=[
            html.Div(
                id="header-row",
                children=[
                    html.H2("CO²Map", id="website-name"),
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[{"label": str(country), "value": country} for country in {"France", "Germany", "United States"}],
                        placeholder="Sélectionnez un pays",
                    )
                ]
            ),
            html.Hr(),
            html.Div(
                id="header-slider",
                children=[
                    dcc.Slider(
                        years.min(),
                        years.max(),
                        step=None,
                        value=years.max(),
                        marks={str(year): str(year) for year in years},
                        id='year-slider'
                    )
                ]
            )
        ]
    )

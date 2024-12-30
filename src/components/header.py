from dash import html, dcc

def get_header():
    return html.Div(
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
            html.Div(
                id="header-slider",
                children=[
                    dcc.Slider(
                        1960,
                        2010,
                        step=2,
                        value=1986,
                        marks={year: str(year) for year in range(1960, 2011)},
                        id='year-slider'
                    )
                ]
            )
        ]
    )

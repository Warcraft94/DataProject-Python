from dash import html, dcc

def create_header(years: list) -> html.Header:
    """
    Crée le header de l'application

    Args:
        years (list): Liste des années disponibles
    
    Returns:
        html.Header: Header de l'application
    """

    return html.Header(
        id="header",
        children=[
            html.Div(
                id="header-row",
                children=[
                    html.H2("CO²Map", id="website-name"),
                    # TODO : Ajouter le dropdown pour les pays dynamiquement si utilisé
                    # dcc.Dropdown(
                    #     id="country-dropdown",
                    #     options=[{"label": str(country), "value": country} for country in {"France", "Germany", "United States"}],
                    #     placeholder="Sélectionnez un pays",
                    # )
                ]
            ),
            html.Hr()
        ]
    )

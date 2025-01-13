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
        className="header",
        children=[
            html.Div(
                className="header-row",
                children=[
                    html.H2("CO²Map", className="website-name"),
                    html.H5("Visualisateur des émissions de CO² dans le monde", className="website-description"),
                ]
            ),
            html.Hr()
        ]
    )

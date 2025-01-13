from dash import html

def create_footer() -> html.Footer:
    """
    Crée le footer de l'application

    Returns:
        html.Footer: Footer de l'application
    """

    return html.Footer(
        className="footer",
        children=[
            html.Div([
                "© 2024 Poulain Kyrian & Fauconnier Aurélien, tous droits réservés.",
                html.Br(),
                "Fait en utilisant Dash et Plotly",
            ]),
            html.Div([
                html.A("Github du projet", href="https://github.com/Warcraft94/DataProject-Python", target="_blank"),
            ])
        ]
    )
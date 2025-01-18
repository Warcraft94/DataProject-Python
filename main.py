import dash
from src.pages import SimpleDashboard
from config import DASH_DEBUG_MODE
from src.utils import get_data, clean_data, clean_geojson, load_data

##################################################################
############################## MAIN ##############################
##################################################################
if __name__ == '__main__':

    # Récupère les données d'énergie via l'API Kaggle.
    print("Téléchargement du jeu de données...")
    get_data()

    # Nettoie les fichiers de données et de geojson suivant les règles définies et les données nécessaires pour l'application.
    print("Nettoyage des données geojson...")
    clean_geojson()
    print("Nettoyage des données csv...")
    clean_data()

    # Charge les données d'énergie et de géojson nettoyées.
    energy_data, geojson_data = load_data()

    # Créer l'instance de la classe SimpleDashboard.
    print("Lancement de l'application web...")
    dashboard_page = SimpleDashboard(energy_data, geojson_data)

    # Initialisation de l'application Dash avec le layout et les callbacks.
    app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])      # Initialisation de l'application Dash.
    app.title = "CO²Map"                                                        # Titre de l'application.
    app.layout = dashboard_page.create_layout()                                 # Layout de l'application.
    dashboard_page.setup_callbacks(app)                                         # Configuration des callbacks pour l'interaction et les updates des graphiques.

    # Lance l'application web dash.
    app.run_server(debug=DASH_DEBUG_MODE)
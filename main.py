import dash
import pandas
import os
import json
from src.pages import SimpleDashboard
from config import DASH_DEBUG_MODE
from src.utils import clean_data, clean_geojson

def load_data() -> tuple:
    """
    Récupère les fichiers de données

    Returns:
        Dataframe: Dataframe des données d'énergies et d'émissions de CO2 par pays
        dict: Dictionnaire geojson des pays
    """

## TODO utiliser une fonction commune ici (car déjà quasiment identique à src/utils/clean_data.py)
    # Récupère le chemin absolu du répertoire où le script s'exécute
    current_dir = os.path.dirname(__file__) 
    
    # Construit le chemin d'accès au fichier geojson et au fichier de données csv
    geojson_path = os.path.join(current_dir, "data/cleaned/cleaned_countries.geojson")
    data_path = os.path.join(current_dir, "data/cleaned/cleaned_energy.csv")

    # Récupère le fichier geojson sous forme de dict()
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
    
    # Récupère le fichier de données sous forme de dataframe
    energy_data = pandas.read_csv(data_path, sep=';')

    return energy_data, geojson_data

#
# Main
#
if __name__ == '__main__':

    # Nettoie les fichiers de données et de geojson suivant les règles définies et les données nécessaires pour l'application
    # print("Nettoyage des données geojson...")
    # clean_geojson()
    # print("Nettoyage des données csv...")
    # clean_data()

    # Récupère les données d'énergie et de géojson utilisées par l'application
    energy_data, geojson_data = load_data()

    # Créer l'instance de la classe SimpleDashboard
    dashboard_page = SimpleDashboard(energy_data, geojson_data)

    print("Lancement de l'application web...")

    # Initialisation de l'application Dash
    app = dash.Dash(__name__)

    # Titre de l'application
    app.title = "CO²Map"
    
    # Layout de l'application
    app.layout = dashboard_page.create_layout()

    # Configuration des callbacks pour l'interaction et les updates des graphiques
    dashboard_page.setup_callbacks(app)

    # Lance l'application web dash
    app.run_server(debug=DASH_DEBUG_MODE)
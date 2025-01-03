import plotly_express as px
import dash
import pandas as pd
import os
import json
from dash import dcc, html
from dash.dependencies import Input, Output
from src.utils import clean_geojson
from src.pages import SimpleDashboard
from config import DASH_DEBUG_MODE

#
# Data
#
def load_data():
    """Récupère les fichiers de données

    Returns:
        pd.Dataframe: Dataframe des données d'énergies et d'émissions de CO2 par pays
        dict: Dictionnaire geojson des pays
    """
    # Récupère le chemin absolu du répertoire où le script s'exécute
    current_dir = os.path.dirname(__file__) 
    
    # Construit le chemin d'accès au fichier geojson
    geojson_path = os.path.join(current_dir, "data/cleaned/cleaned_countries.geojson")
    # Récupère le fichier geojson sous forme de dict()
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
        
    # Construit le chemin d'accès au fichier csv
    data_path = os.path.join(current_dir, "data/cleaned/formatted_energy.csv")
    energy_data = pd.read_csv(data_path, sep=';')
    
    energy_data["CO2_emission"] = pd.to_numeric(energy_data["CO2_emission"])
    energy_data["Energy_consumption"] = pd.to_numeric(energy_data["CO2_emission"])
    energy_data["Energy_production"] = pd.to_numeric(energy_data["CO2_emission"])
    
    return energy_data, geojson_data

#
# Main
#
if __name__ == '__main__':
    # Récupère les données
    energy_data, geojson_data = load_data()

    # Créer l'instance de la classe SimpleDashboard
    dashboard_page = SimpleDashboard(energy_data, geojson_data)

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
    
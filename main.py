import plotly_express as px
import dash
import pandas as pd
import os
import json
from dash import dcc, html
from dash.dependencies import Input, Output
from src.utils import clean_geojson
from src.pages import create_home_page
from src.components import SimpleDashboard

#
# Data
#
"""
year = 2002

years = pop_data["Year"].unique()
data = {year:pop_data.query("Year == @year") for year in years}

print(years)

#
# nos données
#
# Récupération de la colonne 'Code Département' contenant les codes INSEE des communes
countries_code = pop_data['Country']

# Création d'un masque pour ne récupérer que les communes d'IDF
mask = ( ( countries_code.str.startswith('World') ) )

# Filtrage avec le masque pour ne pas prendre = World
pop_data = pop_data[~mask]

energy_type = pop_data['Energy_type']
mask2 = ( ( energy_type.str.startswith('all_energy_types') ) ) # Filtrage avec le masque pour ne pas prendre = all_energy_types
pop_data = pop_data[mask2]

pop_data['ADMIN'] = pop_data.pop('Country')
pop_data["CO2_emission"] = pandas.to_numeric(pop_data["CO2_emission"])

df = pop_data
"""

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
    dashboard = SimpleDashboard(energy_data, geojson_data)
    # Lance l'application web dash
    dashboard.run()
    
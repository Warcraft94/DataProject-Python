import os
import json
import pandas
from config import DATAS_CLEANED_PATH, GEOJSON_CLEANED_NAME, DATA_CLEANED_NAME

def get_path(folder_path: str, file_name: str) -> str:
    """
    Récupère le chemin vers un fichier à partir de son nom et du chemin vers le répertoire le contenant.

    Args:
        folder_path (str): Chemin du répertoire.
        file_name (str): Nom du fichier.

    Returns:
        str: Chemin complet vers le fichier.
    """

    # Récupère le chemin du répertoire actuel.
    base_dir = os.path.dirname(__file__)

    # Retourne le chemin complet du fichier.
    return os.path.join(base_dir, folder_path, file_name)


def load_data() -> tuple:
    """
    Récupère les fichiers de données et de geojson nettoyés.

    Returns:
        Dataframe: Dataframe du fichier de données.
        dict: Dictionnaire geojson des pays.
    """

    # Construit le chemin d'accès au fichier geojson et au fichier de données csv.
    geojson_path = get_path("../../"+DATAS_CLEANED_PATH, GEOJSON_CLEANED_NAME)
    data_path = get_path("../../"+DATAS_CLEANED_PATH, DATA_CLEANED_NAME)

    # Récupère le fichier geojson sous forme de dictionnaire.
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
    
    # Récupère le fichier de données sous forme de Dataframe.
    energy_data = pandas.read_csv(data_path, sep=';')

    return energy_data, geojson_data
import geopandas, pandas
import os
from config import *

def get_source_and_target_paths(source_name: str, target_name: str) -> tuple:
    """
    Récupère les chemins vers les fichiers source et cible à partir de leur nom

    Args:
        source_name (str): Nom du fichier source
        target_name (str): Nom du fichier cible

    Returns:
        tuple: Chemins vers les fichiers source et cible
    """

    base_dir = os.path.dirname(__file__)

    source_path = os.path.join(base_dir, "..", "..", DATAS_RAW_PATH, source_name)
    target_path = os.path.join(base_dir, "..", "..", DATAS_CLEANED_PATH, target_name)

    return source_path, target_path


def clean_geojson() -> None:
    """
    Nettoie le fichier geojson des pays
    """

    source_path, target_path = get_source_and_target_paths(GEOJSON_RAW_NAME, GEOJSON_CLEANED_NAME)
    

    # Lecture du fichier global
    countries = geopandas.read_file(source_path)

    # Liste des lignes pays modifiées
    modified_rows = []

    # Pour tout les pays sauf le monde
    for country in countries["ADMIN"]:
        if country != "World":
            
            # Selectionne les lignes du pays sélectionné
            country_selected = countries[countries["ADMIN"].str.startswith(country)]
            
            # Remplace les noms de pays par les noms utilisés dans le fichier de données
            if country_selected["ADMIN"].iloc[0] in MAPPED_COUNTRIES_NAMES:
                country_selected = country_selected.copy()  # Copie pour éviter les avertissements 
                country_selected.loc[:, "ADMIN"] = country_selected["ADMIN"].replace(MAPPED_COUNTRIES_NAMES)
            
            # Ajoute les lignes modifiées à la liste
            modified_rows.append(country_selected)

    # Concatène les lignes modifiées pour obtenir le fichier nettoyé
    cleaned_countries = pandas.concat(modified_rows)

    # Ecriture du fichier nettoyé dans path cible
    cleaned_countries.to_file(target_path, driver="GeoJSON")


def clean_data() -> None:
    """
    Nettoie le fichier de données
    """

    source_path, target_path = get_source_and_target_paths(DATA_RAW_NAME, DATA_CLEANED_NAME)

    # Lecture du fichier
    energy_data = pandas.read_csv(source_path, sep=';')

    # Mapping des données concernant le type d'énergie pour les avoirs en français
    energy_data = energy_data.replace({"Energy_type": MAPPED_ENERGY_TYPES})

    for column in DATA_COLUMNS_TO_CONVERT_INTO_NUMERICS:
        # Remplace les virgules par des points
        energy_data[column] = energy_data[column].astype(str).str.replace(",", ".", regex=False)

        # Convertit les valeurs en numérique et remplace les valeurs invalides par NaN
        energy_data[column] = pandas.to_numeric(energy_data[column], errors="coerce")

    # Supprime les colonnes inutiles pour notre application
    energy_data = energy_data.drop(columns=DATA_COLUMNS_TO_REMOVE)

    # Supprime toutes les lignes avec au moins une valeur manquante (NaN)
    energy_data = energy_data.dropna()

    # Ecriture du fichier nettoyé dans path cible
    energy_data.to_csv(target_path, sep=';', index=False)
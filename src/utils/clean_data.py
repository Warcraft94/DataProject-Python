import geopandas, pandas
from config import DATAS_RAW_PATH, DATAS_CLEANED_PATH, GEOJSON_RAW_NAME, GEOJSON_CLEANED_NAME, DATA_RAW_NAME, DATA_CLEANED_NAME, MAPPED_COUNTRIES_NAMES, MAPPED_ENERGY_TYPES, DATA_COLUMNS_TO_CONVERT_INTO_NUMERICS, DATA_COLUMNS_TO_REMOVE
from src.utils.common_functions import get_path


def clean_geojson() -> None:
    """
    Nettoie le fichier geojson des pays
    """

    source_path = get_path("../"+"../"+DATAS_RAW_PATH, GEOJSON_RAW_NAME)
    target_path = get_path("../"+"../"+DATAS_CLEANED_PATH, GEOJSON_CLEANED_NAME)

    # Lecture du fichier global
    countries = geopandas.read_file(source_path)

    # Liste des lignes pays modifiées
    modified_rows = []

    # Pour tout les pays sauf le monde
    for country in countries["name"]:
        if country != "World":
            
            # Selectionne les lignes du pays sélectionné
            country_selected = countries[countries["name"].str.startswith(country)]
            
            # Remplace les noms de pays par les noms utilisés dans le fichier de données
            if country_selected["name"].iloc[0] in MAPPED_COUNTRIES_NAMES:
                country_selected = country_selected.copy()  # Copie pour éviter les avertissements 
                country_selected.loc[:, "name"] = country_selected["name"].replace(MAPPED_COUNTRIES_NAMES)
            
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

    source_path = get_path("../"+"../"+DATAS_RAW_PATH, DATA_RAW_NAME)
    target_path = get_path("../"+"../"+DATAS_CLEANED_PATH, DATA_CLEANED_NAME)

    # Lecture du fichier
    energy_data = pandas.read_csv(source_path, sep=',')

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
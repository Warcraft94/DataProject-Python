############################## FICHIER DE CONFIGURATION ##############################
#           Ce fichier contient les variables de configuration du projet             #
######################################################################################

# Lancer l'application en mode debug
DASH_DEBUG_MODE = True

# Paths vers les fichiers de données
DATAS_BASE_PATH = "data"
DATAS_RAW_PATH = f"{DATAS_BASE_PATH}/raw"
DATAS_CLEANED_PATH = f"{DATAS_BASE_PATH}/cleaned"

# Noms des fichiers de données
DATA_RAW_NAME = "energy.csv" # TODO: surement a changer pour un zip
DATA_CLEANED_NAME = "cleaned_energy.csv"
GEOJSON_RAW_NAME = "countries.geo.json"
GEOJSON_CLEANED_NAME = "cleaned_countries.geo.json"

################################################################
############### REGLES DE NETTOYAGE DES DONNEES ################
################################################################
# Noms des pays à mapper pour correspondre aux noms utilisés dans le fichier de données
MAPPED_COUNTRIES_NAMES = {
    "United States of America" : "United States",
    "Republic of Congo" : "Congo-Brazzaville",
    "Democratic Republic of the Congo" : "Congo-Kinshasa",
    "United Republic of Tanzania" : "Tanzania",
    "Myanmar" : "Burma", #(Burma = Birmanie)
    "Republic of Serbia" : "Former Serbia and Montenegro"
}

# Colonnes à supprimer du fichier de données car inutiles pour l'application
DATA_COLUMNS_TO_REMOVE = ["GDP", "Energy_intensity_per_capita", "Energy_intensity_by_GDP", "Energy_production"]

# Colonnes à convertir en numériques dans le fichier de données
DATA_COLUMNS_TO_CONVERT_INTO_NUMERICS = ["CO2_emission", "Energy_consumption"]

# Noms des types d'énergies à mapper pour la version française
MAPPED_ENERGY_TYPES = {
    "coal" : "Charbon",
    "natural_gas" : "Gaz naturels",
    "petroleum_n_other_liquids" : "Pétrole et autres liquides",
    "nuclear" : "Nucléaires",
    "renewables_n_other" : "Renouvelables et autres"
}

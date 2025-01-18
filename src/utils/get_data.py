from kaggle.api.kaggle_api_extended import KaggleApi
from config import DATAS_RAW_PATH

def get_data() -> None:
    """
    Récupère le fichier de données CSV via l'API Kaggle.
    """

    # Initialise l'API Kaggle (nécessite un fichier de token "kaggle.json" dans le dossier ~/.kaggle/ sous Linux ou C:\Users\<user>\.kaggle\ sous Windows).
    api = KaggleApi()
    api.authenticate()

    # Jeu de données à télécharger.
    dataset = "lobosi/c02-emission-by-countrys-grouth-and-population"

    # Téléchargement du jeu de données.
    api.dataset_download_files(dataset, path="./"+DATAS_RAW_PATH, unzip=True)
from typing import Callable
from pandas import DataFrame, Series
from functools import wraps
from numpy import ndarray

class DataObject:
    """
    Classe chargée de la gestion des données (coupe, trie, sépare les données, ..).
    """

    def __init__(self, energy_data: DataFrame, years: ndarray) -> None:
        """
        Constructeur de la classe DataObject.

        Args:
            energy_data (DataFrame): Contient les données d'émissions de CO2 par type d'énergie et de production et consommation d'énergie, par pays et par année.
            years (ndarray): Plage d'années présente dans le fichier de données.
        """
        
        self.energy_data : DataFrame = energy_data
        
        # Crée un dictionnaire avec pour clé les années et pour valeur les lignes où la colonne Year correspond à la clé.
        self.energy_data_per_year : dict = {year:energy_data.query("Year == @year") for year in years} # Year est la colonne des années dans le tableau, @year est une référence à la variable year défini dans la boucle for.
    
    def filter_by_column(func: Callable) -> Callable:   # type: ignore
        @wraps(func) # Permet de conserver le nom de la fonction d'origine, sa docstring, ..
        def wrapper(self, *args, **kwargs):
            # Enlève les potentiels colonnes spécifiées dans kwargs des paramètres de la fonction.
            columns = kwargs.pop('columns', None)  # Récupère les colonnes de kwargs, si présentes.

            # Appelle la fonction décoré.
            result = func(self, *args, **kwargs)

            # Si des colonnes spécifiques sont en paramètre de kwargs.
            if columns:
                result = result[list(columns)]  # Filtre les colonnes spécifiques.
            return result
        return wrapper
    
    @filter_by_column
    def get_data(self, *columns: str, year: int=0) -> DataFrame:
        """
        Retourne le Dataframe (pour une année et des colonnes spécifique si précisé en paramètre).
        
        Args:
            columns (*str): Liste des colonnes à extraire.
            year (int): Année sélectionné (optionel).

        Returns:
            DataFrame: Contient les colonnes du Dataframe self.energy_data en paramètres.
        """
        
        # Si une année est spécifiée, retourne les données de cette année.
        if year != 0:
            return self.energy_data_per_year[year]
        return self.energy_data
    
    @filter_by_column
    def get_data_per_country(self, country: str, *columns: str, year: int=0) -> DataFrame:
        """
        Retourne les lignes du Dataframe pour un pays spécifique (et pour une année et des colonnes spécifiques si précisé en paramètre).

        Args:
            country (str): Pays sélectionné.
            columns (*str): Liste des colonnes à extraire.
            year (int): Année sélectionné (optionel).
            
        Returns:
            Dataframe: Contient les données (emissions CO2, production d'énergie, consommation d'énergie, ..) pour le pays sélectionné.
        """
        
        # Si une année est spécifiée, retourne les données de cette année.
        if year != 0:
            return self.energy_data_per_year[year][self.energy_data_per_year[year]['Country'] == country]    
        return self.energy_data[self.energy_data['Country'] == country]
    
    @staticmethod
    def get_mask(col: DataFrame, mask: str) -> Series:
        """
        Génère un masque sur une colonne spécifique d'un Dataframe.

        Args:
            col (DataFrame): La colonne du Dataframe sur laquelle appliquer un masque.
            mask (str): String correspondant à la valeur à masquer.

        Returns:
            Series: Le masque à appliquer sur le Dataframe complet.
        """
        
        return (( col.str.startswith(mask) ))
        
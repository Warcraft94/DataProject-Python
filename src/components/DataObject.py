import pandas as pd

from functools import wraps

class DataObject:
    """
    Classe chargé de la gestion des données (coupe, trie, sépare les données, ..)
    """
    def __init__(self, energy_data: pd.DataFrame, years: list):
        """Constructeur de la classe DataObject

        Args:
            energy_data (list): Tableau des énergies produites, consommés et de l'émission de CO2 par pays et par année
            years (list): Plage d'années présente dans le tableau des énergies
        """
        # Créé un dictionnaire avec pour clé les années et pour valeur les lignes où la colonne Year correspond à la clé
        self.energy_data = {year:energy_data.query("Year == @year") for year in years} # Year est la colonne des années dans le tableau, @year est une référence à la variable year défini dans la boucle for 
        # Année sélectionné, par défaut on prend la première année de la plage
        self.year = years[len(years)-1]
        
    def change_data_for_year(self, year: int):
        """Change l'année sélectionné et renvoi les lignes du Dataframe self.energy_data pour cette année

        Args:
            year (int): année sélectionné

        Returns:
            pd.Dataframe: contient les données (emissions CO2, production d'énergie, consommation d'énergie, ..) par pays pour l'année sélectionné
        """
        self.year = year
        return self.energy_data[self.year]
    
    def get_data_columns(self, *args: str):
        """Retourne les colonnes en paramètres du Dataframe self.energy_data

        Returns:
            pd.Dataframe: contient les colonnes du Dataframe self.energy_data en paramètres
        """
        return self.energy_data[self.year][list(args)]
    
    def filters_on_data_per_country(func):
        @wraps(func) # Permet de conserver le nom de la fonction d'origine, sa docstring, ..
        def wrapper(country: str, emission_type_filter: bool = False, energy_filter: bool = False):
            # Appelle la fonction get_data_per_country
            tab = func(country)
            # Si on récupère uniquement les données des types d'émissions de CO2
            if emission_type_filter:
                # TODO : filtre des données des types d'émissions de CO2
                # return tab.drop(columns=['Other'])
                return tab[['Energy_type', 'CO2_emission']]
            # Si on récupère uniquement les données de production et consommation d'énergie
            elif energy_filter:
                # TODO : filtre des données d'énergie (production et consommation)
                return tab[['Energy_consumption', 'Energy_production']]
            return result
        return wrapper
    
    @filters_on_data_per_country
    def get_data_per_country(country: str):
        """Renvoi les lignes du Dataframe self.energy_data correspondant au pays en paramètre

        Args:
            country (str): Pays sélectionné
            
        Returns:
            pd.Dataframe: contient les données (emissions CO2, production d'énergie, consommation d'énergie, ..) pour le pays sélectionné
        """
        return energy_data[self.year][energy_data[self.year]['Country'] == country]
    
    @staticmethod
    def get_mask(col: pd.DataFrame, mask: str):
        
        return (( col.str.startswith(mask) ))
        
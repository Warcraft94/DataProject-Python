import plotly_express as px
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

from ..utils.DataObject import DataObject
from ..components.footer import create_footer
from ..components.header import create_header

class SimpleDashboard:
    """Classe chargé de générer le Dashboard 
    """
    
    def __init__(self, energy_data: pd.DataFrame, geojson_data: dict):
        """Constructeur de la classe SimpleDashboard

        Args:
            energy_data (pd.DataFrame): contient les données d'émissions de CO2 par type d'énergie et de production et consommation d'énergie, par pays et par année
            geojson_data (dict): contient les données de localisation géographique des pays
        """
        # Récupère toutes les années uniques dans le tableau energy_data
        years = energy_data["Year"].unique()
        # DataObject contenant les différents tableaux de données utilisés pour les graphiques
        self.data = DataObject(energy_data, years)
        self.geojson_data = geojson_data
        self.years = years
        
        # Année sélectionné pour l'affichage des graphiques, par défaut on prend la première année de la plage
        self.year = years[len(years)-1]
        
    def create_layout(self):
        """Crée le layout du site avec la disposition des différents composants
        """
        
        # TODO : Tabulations/Onglets à faire
        
        fig1 = self.create_scatter_plot(self.year)
        fig2 = self.create_pie_plot(self.year)
        fig3 = self.create_choropleth_map(self.year)
        
        return html.Div(id="main-container", children=[
            create_header(self.years),

            # Titre de la page
            # html.H1(
            #     id="title",
            #     style={'textAlign': 'center', 'color': '#7FDBFF'}
            # ),

            dcc.Tabs(value='tab1', children=[
                dcc.Tab(label='Nuage de points', value='tab1', className="custom-tab", selected_className='custom-tab--selected', children=[
                    # Nuage de points (Consommation d'énergie comparé à émission de CO2 de chaque pays)
                    dcc.Graph(
                        id='graph1',
                        figure=fig1
                    )
                ]),
                dcc.Tab(label='Camembert', value='tab2', className="custom-tab", selected_className='custom-tab--selected', children=[
                    # Graphique circulaires (Emission de CO2 par type d'énergie)
                    dcc.Graph(
                        id='graph2',
                        figure=fig2
                    ),
                ]),
                dcc.Tab(label='Carte choroplète', value='tab3', className="custom-tab", selected_className='custom-tab--selected', children=[
                    # Carte choroplète (Emission de CO2 par pays)
                    dcc.Graph(
                        id='graph3',
                        figure=fig3
                    ),
                ]),
            ]),
                   
            create_footer()
        ])
    
    def setup_callbacks(self, app):
        """Configure les callbacks pour update les graphiques en fonction des entrées
        """
        
        @app.callback(
            [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure')],
            [Input('year-slider', 'value')]
        )
        # Update tous les graphiques à chaque changement d'année
        def update_graphs(selected_year):
            self.data.change_data_for_year(selected_year)
            fig1 = self.create_scatter_plot(selected_year)
            fig2 = self.create_pie_plot(selected_year)
            fig3 = self.create_choropleth_map(selected_year)
            return fig1, fig2, fig3
        
    def create_scatter_plot(self, selected_year: int):
        """Crée un graphique en nuage de points représentant l'énergie consommé par rapport à l'émission de CO2 pour chaque pays, pour l'année sélectionnée

        Args:
            selected_year (int): année sélectionné

        Returns:
            px.graph_objects.Figure: graphique en nuage de points
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data
        df = self.data.get_data_columns('Country', 'Energy_consumption', 'Energy_production', 'CO2_emission', 'Energy_type', 'Year')
        
        # Création d'un masque pour ne pas récupérer l'instance "World"
        mask = self.data.get_mask(df['Country'], 'World')
        df = df[~mask] # Enlève l'instance "World" du Dataframe
        
        # Création d'un masque pour ne récupérer que le type "all_energy_types"
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask] # Garde que l'instance de "all_energy_types" pour chaque pays du Dataframe
        
        # Crée un graphique de nuages de points
        fig = px.scatter(
            df, 
            x="Energy_consumption", 
            y="CO2_emission", 
            color="Country", 
            size="Year", 
            hover_name="Country",
            title="Emissions de CO2 par rapport à la consommation d'énergie par pays"   # Le titre de la figure
        )
        
        return fig
    
    def create_pie_plot(self, selected_year: int):
        """Crée un graphique circulaire (camembert) représentant le % d'émissions de CO2 pour chaque type d'énergie dans le Monde pour l'année sélectionnée

        Args:
            selected_year (int): année sélectionné

        Returns:
            px.graph_objects.Figure: graphique circulaire
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data
        df = self.data.get_data_per_country('World', 'Energy_type', 'CO2_emission')   
        
        # Création d'un masque pour ne pas récupérer l'instance "all_energy_types"
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[~mask] # Enlève l'instance "all_energy_types" du Dataframe
        
        # Crée un graphique circulaire (camembert)
        fig = px.pie(
            df,
            names = "Energy_type",
            values = "CO2_emission",
            labels = "Energy_type",
            color_discrete_sequence=['red', 'blue', 'green', 'orange'],
            title="Emissions de CO2 par énergie",                           # Le titre de la figure
            #hovertemplate = "%{label}: <br>Popularity: %{percent} </br> %{text}"
        )
        
        return fig

    def create_choropleth_map(self, selected_year: int):
        """Crée une carte choroplète des émissions de CO2 pour chaque pays, pour l'année sélectionnée

        Args:
            selected_year (int): année sélectionné

        Returns:
            px.graph_objects.Figure: figure choropleth
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data
        df = self.data.get_data_columns('Country', 'CO2_emission', 'Energy_type')
        
        # Création d'un masque pour ne pas récupérer l'instance "World"
        mask = self.data.get_mask(df['Country'], 'World')
        df = df[~mask] # Enlève l'instance "World" du Dataframe
        
        # Création d'un masque pour ne récupérer que le type "all_energy_types"
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask] # Garde que l'instance de "all_energy_types" pour chaque pays du Dataframe
        
        fig = px.choropleth_mapbox(
            df,
            geojson=self.geojson_data,                      # GeoJSON file
            color="CO2_emission",                           # Colonne du Dataframe qui détermine la variation de couleur par rapport aux valeurs
            locations="Country",                            # Colonne du Dataframe qui détermine le pays
            featureidkey="properties.ADMIN",                # Clé du GeoJson pour trouver le pays associé
            color_continuous_scale="YlGn",                  # Echelle de couleur
            range_color=[0, 15000],                         # Min et max de l'échelle de couleur
            mapbox_style="carto-positron",                  # Style de la Map
            zoom=2,                                         # Zoom initial sur la Map
            center={"lat": 0, "lon": 0},                    # Centre de la Map
            title="Carte des émissions de CO2 par pays",    # Le titre de la figure
        )
        
        return fig
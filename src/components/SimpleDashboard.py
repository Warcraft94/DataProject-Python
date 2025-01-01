import plotly_express as px
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from .DataObject import DataObject
from .footer import create_footer
from .header import create_header

class SimpleDashboard:
    """
    Classe chargé de générer le Dashboard 
    """
    def __init__(self, energy_data: pd.DataFrame, geojson_data: dict):
        
        # Récupère toutes les années uniques dans le tableau energy_data
        years = energy_data["Year"].unique()
        # DataObject contenant les différents tableaux de données utilisés pour les graphiques
        self.data = DataObject(energy_data, years)
        self.geojson_data = geojson_data
        self.years = years
        
        # Année sélectionné pour l'affichage des graphiques, par défaut on prend la première année de la plage
        self.year = years[len(years)-1]
        
        # Initialisation de l'application Dash
        self.app = dash.Dash(__name__)
        
        # Layout de l'application
        self.app.layout = self.create_layout()

        # Configuration des callbacks pour l'interaction et les updates des graphiques
        self.setup_callbacks()
        
    def create_layout(self):
        """
        Crée le layout du site avec la disposition des différents composants
        """
        # TODO : Tabulations/Onglets à faire
        
        fig1 = self.create_scatter_plot(self.year)
        fig2 = self.create_choropleth_map(self.year)
        
        return html.Div([
            create_header(self.years),
            
            # Titre de la page
            html.H1(
                id="title",
                style={'textAlign': 'center', 'color': '#7FDBFF'}
            ),

            # Nuage de points (Consommation d'énergie comparé à émission de CO2 de chaque pays)
            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
            
            # Legend
            html.Div(
                id="legend",
                style={'marginTop': '20px'}
            ),

            # Carte choroplète (Emission de CO2 par pays)
            dcc.Graph(
                id='graph2',
                figure=fig2    
            ),
            
            create_footer(),
        ])
    
    def setup_callbacks(self):
        """
        Configure les callbacks pour update les graphiques en fonction des entrées
        """
        @self.app.callback(
            [Output('graph1', 'figure'), Output('graph2', 'figure')],
            [Input('year-slider', 'value')]
        )
        # Update tous les graphiques à chaque changement d'année
        def update_graphs(selected_year):
            self.data.change_data_for_year(selected_year)
            fig1 = self.create_scatter_plot(selected_year)
            fig2 = self.create_choropleth_map(selected_year)
            return fig1, fig2
        
        # Modèles pour update le graphique 1 et le graphique 2 séparément
        """
        @self.app.callback(
            [Output('graph1', 'figure')],
            [Input('year-slider', 'value')]
        )
        """
        #def update_graph1()
        
        """
        @self.app.callback(
            [Output('graph2', 'figure')],
            [Input('year-slider', 'value')]
        )
        """
        #def update_graph2()
        
    def create_scatter_plot(self, selected_year):
        """
        Crée un graphique en nuage de points comparant l'énergie consommé à l'émission de CO2 de chaque pays, par rapport à l'année sélectionnée
        """
        #df = self.data_object.get_data_for_year(selected_year)
        df = self.data.get_data_columns('Country', 'Energy_consumption', 'Energy_production', 'CO2_emission', 'Year')
        fig = px.scatter(df, x="Energy_consumption", y="CO2_emission", 
                         color="Country", size="Year", hover_name="Country")
        return fig

    def create_choropleth_map(self, selected_year):
        """
        Crée une carte choroplète des émissions de CO2 pour chaque pays par rapport à l'année sélectionnée
        """
        #df = self.data_object.get_data_for_year(selected_year)
        df = self.data.get_data_columns('Country', 'CO2_emission', 'Energy_type')
        
        # Récupération de la colonne 'Country' contenant les pays
        countries_col = df['Country']
        # Création d'un masque pour ne pas récupérer l'instance World
        mask_countries = self.data.get_mask(countries_col, 'World')
        df = df[~mask_countries] # Enlève l'instance World du Dataframe
        
        # Récupération de la colonne 'Energy_type' contenant les types d'énergies
        energy_type_col = df['Energy_type']
        # Création d'un masque pour ne récupérer que le type "all_energy_types"
        mask_energy_type = self.data.get_mask(energy_type_col, 'all_energy_type')
        df = df[mask_energy_type] # Garde que l'instance de all_energy_type pour chaque pays du Dataframe
        
        # Créé un choroplète avec le GeoJSON et les données
        fig = px.choropleth(df, 
                            locations="Country",  # Les pays dans le DataFrame
                            color="CO2_emission",  # Les valeurs des émissions de CO2
                            geojson=self.geojson_data,  # Fichier Geojson
                            featureidkey="properties.ADMIN",  # Clé correspondante dans le GeoJSON (propriété "ADMIN")
                            locationmode="geojson-id",
                            hover_name="Country",  # Affiche le nom du pays lors du survol
                            color_continuous_scale="Viridis",  # Palette de couleurs
                            title="Emissions de CO2 par pays")

        # Met à jour la carte pour avoir les contours du GeoJSON
        fig.update_geos(
            visible=True, 
            showcoastlines=True, 
            coastlinecolor="Black",  # Couleur des côtes
            showland=True, 
            landcolor="lightgray",  # Couleur des terres
            projection_type="mercator"  # Type de projection
        )
        
        return fig

    def run(self):
        """
        Lance l'application Dash
        """
        self.app.run_server(debug=True)
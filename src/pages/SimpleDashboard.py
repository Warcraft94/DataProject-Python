import plotly_express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

from ..utils.DataObject import DataObject
from ..components.footer import create_footer
from ..components.header import create_header

from dash import Dash
from pandas import DataFrame

class SimpleDashboard:
    """Classe chargé de générer le Dashboard 
    """
    
    def __init__(self, energy_data: DataFrame, geojson_data: dict):
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
        
        # Crée un graphique par défaut pour l'affichage
        fig_default = self.create_scatter_plot(self.year)
        
        return html.Div(id="main-container", children=[
            create_header(self.years),

            # Slider pour sélectionner le graphique
            dcc.Tabs(id="tabs", value='tab1', children=[
                dcc.Tab(label='Nuage de points', value='tab1', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Camembert', value='tab2', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Graphique histogramme', value='tab3', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Carte choroplète', value='tab4', className="custom-tab", selected_className='custom-tab--selected'),
            ]),

            html.Div(
                id="slider-container",
                children=[
                    dcc.Slider(
                        self.years.min(),
                        self.years.max(),
                        step=None,
                        value=self.years.max(),
                        marks={str(year): str(year) for year in self.years},
                        id='years-slider'
                    )
                ]
            ),
                

            dcc.Graph(
                id='graph',
                figure=fig_default # Affiche le graphique par défaut
            ),
                   
            create_footer()
        ])
    
    def setup_callbacks(self, app: Dash):
        """Configure les callbacks pour update les graphiques en fonction des entrées
        """
        
        @app.callback(
            [Output('graph', 'figure'), 
             Output('slider-container', 'style')],
            [Input("tabs", "value"),
            Input("years-slider", "value")]
        )
        # Update tous les graphiques à chaque changement d'année
        def update_graphs(selected_tab: str,selected_year: int):
            slider_style = {'display': 'block'}

            if selected_tab == 'tab1':
                fig = self.create_scatter_plot(selected_year)
            elif selected_tab == 'tab2':
                fig = self.create_pie_plot(selected_year)
            elif selected_tab == 'tab3':
                fig = self.create_histogram_plot()
                slider_style = {'display': 'none'}
            elif selected_tab == 'tab4':
                fig = self.create_choropleth_map(selected_year)
            return fig, slider_style
        
    def create_scatter_plot(self, selected_year: int):
        """Crée un graphique en nuage de points représentant l'énergie consommé par rapport à l'émission de CO2 pour chaque pays, pour l'année sélectionnée

        Args:
            selected_year (int): Année sélectionnée

        Returns:
            px.graph_objects.Figure: graphique en nuage de points
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data
        df = self.data.get_data('Country', 'Energy_consumption', 'Energy_production', 'CO2_emission', 'Energy_type', 'Year', year=selected_year)
        
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
            title="Emissions de CO2 par rapport à la consommation d'énergie par pays"   # Titre de la figure
        )
        
        return fig
    
    def create_pie_plot(self, selected_year: int):
        """Crée un graphique circulaire (camembert) représentant le % d'émissions de CO2 pour chaque type d'énergie dans le Monde pour l'année sélectionnée

        Args:
            selected_year (int): Année sélectionnée

        Returns:
            px.graph_objects.Figure: graphique circulaire
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data pour le pays indiqué
        df = self.data.get_data_per_country('World', 'Energy_type', 'CO2_emission', year=selected_year)   
        
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
            title="Emissions de CO2 par énergie",                           # Titre de la figure
            #hovertemplate = "%{label}: <br>Popularity: %{percent} </br> %{text}"
        )
        
        return fig
    
    def create_histogram_plot(self):
        """Crée un graphique histogramme représentant l'évolution par année de l'émission de CO2 comparé à la population dans le Monde

        Returns:
            go.graph_objects.Figure: histogramme
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data pour le pays indiqué
        df = self.data.get_data_per_country('World', 'CO2_emission', 'Population', 'Year', 'Energy_type') 
        
        # Création d'un masque pour ne récupérer que le type "all_energy_types"
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask] # Garde que l'instance de "all_energy_types" pour chaque pays du Dataframe    
        
        # Créer l'instance de la figure
        fig = go.Figure()

        # Barre pour l'évolution de la population
        fig.add_trace(go.Bar(
            x=df['Year'],  # Années sur l'axe X
            y=df['Population'],  # Population pour chaque année
            name='Population',  # Légende
            marker_color='#EB89B5',  # Couleur des barres
            opacity=0.75,  # Transparence des barres
        ))

        # Barre pour l'évolution des émissions de CO2
        fig.add_trace(go.Bar(
            x=df['Year'],  # Années sur l'axe X
            y=df['CO2_emission'],  # Emissions de CO2 pour chaque année
            name='Émissions de CO2',  # Légende
            marker_color='#330C73',  # Couleur des barres
            opacity=0.75,  # Transparence des barres
            yaxis='y2',  # Liaison à un deuxième axe Y
        ))

        # Mise à jour de la mise en page pour les axes et les titres
        fig.update_layout(
            title="Evolution de la Population et des Émissions de CO2 par Année",  # Titre de la figure
            xaxis=dict(
                title="Année",  # Titre de l'axe X
                tickmode='array',  # Mode de ticks personnalisé
                tickvals=df['Year'],  # Utilise les années comme valeur d'intervalle
                ticktext=[str(year) for year in df['Year']],  # Affiche le texte de chaque année pour chaque intervalle
            ),
            yaxis=dict(
                title="Population",  # Titre de l'axe Y pour la population
            ),
            yaxis2=dict(
                title="Émissions de CO2",  # Titre de l'axe Y pour les émissions de CO2
                overlaying='y',  # Superposition avec l'axe Y de la Population
                side='right',  # Positionne l'échelle de l'axe secondaire à droite
            ),
            barmode='group',  # Mode pour afficher les barres des axes Y ensemble
            bargap=0.5,  # Espace/Ecart entre les barres
        )
        
        return fig

    def create_choropleth_map(self, selected_year: int):
        """Crée une carte choroplète des émissions de CO2 pour chaque pays, pour l'année sélectionnée

        Args:
            selected_year (int): Année sélectionnée

        Returns:
            px.graph_objects.Figure: figure choropleth
        """
        
        # Récupère les colonnes spécifiés en paramètres du Dataframe data
        df = self.data.get_data('Country', 'CO2_emission', 'Energy_type', year=selected_year)
        
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
            title="Carte des émissions de CO2 par pays",    # Titre de la figure
        )
        
        return fig
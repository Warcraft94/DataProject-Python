import plotly_express as px
import plotly.graph_objects as go
import numpy as np

from dash import dcc, html
from dash.dependencies import Input, Output
from src.components import create_header, create_footer
from src.utils import DataObject

from plotly.graph_objects import Figure
from dash import Dash
from pandas import DataFrame

class SimpleDashboard:
    """
    Classe chargée de générer le Dashboard.
    """
    
    def __init__(self, energy_data: DataFrame, geojson_data: dict) -> None:
        """
        Constructeur de la classe SimpleDashboard.

        Args:
            energy_data (DataFrame): Contient les données d'émissions de CO2, de production et consommation d'énergie par type d'énergie, par pays et par année.
            geojson_data (dict): Contient les données de localisation géographique des pays.
        """

        # Récupère toutes les années uniques dans le tableau energy_data.
        years = energy_data["Year"].unique()
    
        # Crée une instance de DataObject pour manipuler les données plus facilement dans les graphiques.
        self.data : DataObject = DataObject(energy_data, years)
        self.geojson_data : dict = geojson_data
        self.years : np.ndarray = years

        # Année sélectionnée pour l'affichage des graphiques, par défaut on prend la première année de la plage (la plus récente).
        self.year = years[len(years)-1]
        
    def create_layout(self) -> html.Div:
        """
        Crée le layout de la page avec la disposition des différents composants.
        """

        # Crée un graphique par défaut lors du chargement de la page.
        fig_default = self.create_scatter_plot(self.year)
        
        # Retourne le layout de la page.
        return html.Div(className="main-container", children=[

            # Header de l'application.
            create_header(),

            # Tabulations pour sélectionner le graphique à afficher.
            dcc.Tabs(id="tabs", value='tab1', children=[
                dcc.Tab(label='Nuage de points', value='tab1', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Camembert', value='tab2', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Histogramme', value='tab3', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Double histogramme', value='tab4', className="custom-tab", selected_className='custom-tab--selected'),
                dcc.Tab(label='Carte choroplèthe', value='tab5', className="custom-tab", selected_className='custom-tab--selected'),
            ]),

            # Slider pour sélectionner l'année.
            html.Div(
                className="slider-container",
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
            
            # Conteneur qui affiche le graphique ou une animation de chargement pendant le chargement du graphique.
            html.Div(
                className="graph-container",
                children=[
                    dcc.Loading(
                        className="loading",
                        type="circle",
                        children=[
                            # Graphique affiché en fonction de l'onglet sélectionné.
                            dcc.Graph(
                                className="graph",
                                id='graph',
                                figure=fig_default # Affiche un graphique par défaut.
                            )
                        ]
                    )
                ]
            ),
            
            # Footer de l'application.
            create_footer()
        ])
    
    def setup_callbacks(self, app: Dash) -> None:
        """
        Configure les callbacks pour update les graphiques et le slider en fonction des entrées (onglet sélectionné et année sélectionnée).
        """
        
        @app.callback(
            [Output('graph', 'figure'), 
             Output('slider-container', 'style')],
            [Input("tabs", "value"),
            Input("years-slider", "value")]
        )
        # Fonction qui met à jour les graphiques en fonction de l'onglet sélectionné et de l'année sélectionnée.
        def update_graphs(selected_tab: str,selected_year: int) -> tuple:
            slider_style = {'display': 'block'}

            if selected_tab == 'tab1':
                fig = self.create_scatter_plot(selected_year)
            elif selected_tab == 'tab2':
                fig = self.create_pie_plot(selected_year)
            elif selected_tab == 'tab3':
                fig = self.create_histogram_plot(selected_year)
            elif selected_tab == 'tab4':
                fig = self.create_double_histogram_plot()
                slider_style = {'display': 'none'}
            elif selected_tab == 'tab5':
                fig = self.create_choropleth_map(selected_year)
            return fig, slider_style
        
    def create_scatter_plot(self, selected_year: int) -> Figure:
        """
        Crée un graphique en nuage de points représentant l'énergie consommé par rapport à l'émission de CO2 pour chaque pays, pour l'année sélectionnée.

        Args:
            selected_year (int): Année sélectionnée.

        Returns:
            Figure: Graphique en nuage de points.
        """
        
        # Récupère les colonnes spécifiées en paramètres du Dataframe data pour le pays indiqué et l'année sélectionnée.
        df = self.data.get_data('Country', columns=['Energy_consumption', 'CO2_emission', 'Energy_type', 'Country'], year=selected_year)
        
        # Création d'un masque pour ne pas récupérer les lignes du pays "World".
        mask = self.data.get_mask(df['Country'], 'World')
        df = df[~mask]
        
        # Création d'un masque pour ne récupérer que les lignes où type = "all_energy_types".
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask]
        
        # Configure le nuage de points.
        fig = px.scatter(
            df, 
            x="Energy_consumption", 
            y="CO2_emission", 
            color="Country", 
            hover_data={
                "Country": True,            # Affiche les pays dans l'info-bulle.
            },
        )
        
        # Personnalisation du texte de survol.
        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>Emissions CO2: %{x:.2f} <br>Consommation Energie: %{y:.2f} </br>"  # Texte personnalisé de l'info-bulle.
        )
        fig.update_layout(
            title="Emissions de CO2 par rapport à la consommation d'énergie par pays",   # Titre de la figure.
            xaxis=dict(
                title="Energie consommée (en Quad BTU)",  # Titre de l'axe X.
            ),
            yaxis=dict(
                title="Taux d'émission de CO2 (en MMTonnes)",  # Titre de l'axe Y pour la population.
            ),
            legend=dict(
                title=dict(
                    text="Pays"
                )
            ),

            paper_bgcolor="#111827", # Couleur de fond.
            font_color="#ffffff" # Couleur du texte.
        )
        
        return fig
    
    def create_pie_plot(self, selected_year: int) -> Figure:
        """
        Crée un graphique circulaire (camembert) représentant le % d'émissions de CO2 pour chaque type d'énergie dans le Monde pour l'année sélectionnée.

        Args:
            selected_year (int): Année sélectionnée.

        Returns:
            Figure: Graphique circulaire.
        """
        
        # Récupère les colonnes spécifiées en paramètres du Dataframe pour le Monde par année.
        df = self.data.get_data_per_country('World', columns=['Energy_type', 'CO2_emission'], year=selected_year)   
        
        # Création d'un masque pour ne pas récupérer les lignes où type = "all_energy_types".
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[~mask]

        # Configure le graphique circulaire.
        fig = px.pie(
            df,
            names = "Energy_type",
            values = "CO2_emission",
            color_discrete_sequence=['red', 'blue', 'green', 'orange'],
            title="Emissions de CO2 par énergie",           # Titre de la figure.
        )
        
        # Personnalisation du texte de survol.
        fig.update_traces(
            hovertemplate="Emissions CO2: %{value:.2f} MMTonnes"  # Texte personnalisé de l'info-bulle.
        )

        fig.update_layout(
            paper_bgcolor="#111827", # Couleur de fond.
            font_color="#ffffff" # Couleur du texte.
        )

        return fig
    
    def create_double_histogram_plot(self) -> Figure:
        """
        Crée un graphique histogramme représentant l'évolution par année de l'émission de CO2 comparé à la population dans le Monde.

        Returns:
            Figure: Figure histogramme.
        """
        
        # Récupère les colonnes spécifiées en paramètres du Dataframe pour le Monde par année.
        df = self.data.get_data_per_country('World', columns=['CO2_emission', 'Population', 'Year', 'Energy_type']) 
        
        # Création d'un masque pour ne récupérer que les lignes où type = "all_energy_types".
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask] 
        
        # Créée l'instance de la figure.
        fig = go.Figure()
        
        # Barre pour l'évolution de la population.
        fig.add_trace(go.Bar(
            x=df['Year'],  # Années sur l'axe X.
            y=df['Population'],  # Population pour chaque année.
            name='Population',  # Légende.
            marker_color='#EB89B5',  # Couleur des barres.
            opacity=0.75,  # Transparence des barres.
        ))

        # Barre pour l'évolution des émissions de CO2.
        fig.add_trace(go.Bar(
            x=df['Year'],  # Années sur l'axe X.
            y=df['CO2_emission'],  # Emissions de CO2 pour chaque année.
            name='Émissions de CO2',  # Légende.
            marker_color='#330C73',  # Couleur des barres.
            opacity=0.75,  # Transparence des barres.
            yaxis='y2',  # Liaison à un deuxième axe Y.
        ))

        # Mise à jour de la mise en page pour les axes et les titres.
        fig.update_layout(
            title="Evolution de la Population et des Émissions de CO2 par Année",  # Titre de la figure.
            xaxis=dict(
                title="Année",                                      # Titre de l'axe X.
                tickmode='array',                                   # Mode de ticks personnalisé.
                tickvals=df['Year'],                                # Utilise les années comme valeur d'intervalle.
                ticktext=[str(year) for year in df['Year']],        # Affiche le texte de chaque année pour chaque intervalle.
            ),
            yaxis=dict(
                title="Population (Millions)",                      # Titre de l'axe Y pour la population.
            ),
            yaxis2=dict(
                title="Émissions de CO2 (MMTonnes)",                # Titre de l'axe Y pour les émissions de CO2.
                overlaying='y',                                     # Superposition avec l'axe Y de la Population.
                side='right',                                       # Positionne l'échelle de l'axe secondaire à droite.
            ),
            barmode='group',                                        # Mode pour afficher les barres des axes Y ensemble.
            bargap=0.5,                                             # Espace/Ecart entre les barres.

            paper_bgcolor="#111827",                                # Couleur de fond.
            font_color="#ffffff"                                    # Couleur du texte.
        )
        
        # Personnalisation du texte de survol.
        fig.update_traces(
            hovertemplate="%{value:.2f}"  # Texte personnalisé de l'info-bulle.
        )
        
        return fig

    def create_choropleth_map(self, selected_year: int) -> Figure:
        """
        Crée une carte choroplète des émissions de CO2 pour chaque pays, pour l'année sélectionnée.

        Args:
            selected_year (int): Année sélectionnée.

        Returns:
            Figure: Figure choropleth.
        """
        
        # Récupère les colonnes spécifiées en paramètres du Dataframe data pour le pays indiqué et l'année sélectionnée.
        df = self.data.get_data('Country', columns=['CO2_emission', 'Energy_type', 'Country', 'Population'], year=selected_year)
       
        # Création d'un masque pour ne pas récupérer les lignes du pays "World".
        mask = self.data.get_mask(df['Country'], 'World')
        df = df[~mask]
        
        # Création d'un masque pour ne récupérer que les lignes où type = "all_energy_types".
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask]
        
        # On passe la colonne Population en Mperson (Milion of person).
        df['Population'] = df['Population'] / 1000
        
        # Configure la map choroplèthe.
        fig = px.choropleth_mapbox(
            df,
            geojson=self.geojson_data,                      # GeoJSON file.
            color="CO2_emission",                           # Colonne du Dataframe qui détermine la variation de couleur par rapport aux valeurs.
            locations="Country",                            # Colonne du Dataframe qui détermine le pays.
            featureidkey="properties.name",                 # Clé du GeoJson pour trouver le pays associé.
            color_continuous_scale="YlGn",                  # Echelle de couleur.
            range_color=[0, 15000],                         # Min et max de l'échelle de couleur.
            mapbox_style="carto-positron",                  # Style de la Map.
            zoom=2,                                         # Zoom initial sur la Map.
            center={"lat": 0, "lon": 0},                    # Centre de la Map.
            title="Carte des émissions de CO2 par pays",    # Titre de la figure.
            hover_data={
                "Country": True,                            # Affiche les pays.
                "CO2_emission": True,                       # Affiche les émissions de CO2.
                "Population": True,                         # Affiche la population.
            },
        )
        
        # Personnalisation du texte de survol.
        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b> <br>Émissions de CO2: %{customdata[1]:.2f} MMTonnes<br>Population: %{customdata[2]:.2f} M"
        )

        fig.update_layout(
            paper_bgcolor="#111827", # Couleur de fond.
            font_color="#ffffff" # Couleur du texte.
        )
        
        return fig
    
    def create_histogram_plot(self, selected_year: int) -> Figure:
        """
        Crée un histogramme des émissions de CO2 avec des intervalles personnalisés pour chaque pays, pour l'année sélectionnée.

        Args:
            selected_year (int): Année sélectionnée.

        Returns:
            Figure: Figure histogramme.
        """

        # Récupère les colonnes spécifiées en paramètres du Dataframe data pour le pays indiqué et l'année sélectionnée.
        df = self.data.get_data(columns=['CO2_emission', 'Country', 'Population', 'Year', 'Energy_type'], year=selected_year) 
        
        # Création d'un masque pour ne pas récupérer les lignes du pays "World".
        mask = self.data.get_mask(df['Country'], 'World')
        df = df[~mask]
        
        # Création d'un masque pour ne récupérer que les lignes où type = "all_energy_types".
        mask = self.data.get_mask(df['Energy_type'], 'all_energy_types')
        df = df[mask]
        
        multiplier = 20 # Multiplie le nombre d'intervalles pour une meilleure visualisation.
        max_value = df['CO2_emission'].max()
        
        # Filtre les valeurs positives uniquement pour éviter tout soucis avec logarithme.
        df_filtered = df[df['CO2_emission'] != 0]
        
        # Calcul du logarithme des données pour créer une échelle dynamique.
        log_data = np.log10(df_filtered['CO2_emission'])      
        # Définit des intervalles logarithmiques sur la base du log des données.
        log_intervals = np.linspace(log_data.min(), log_data.max(), multiplier)

        # Convertit les bornes logaritmiques en valeurs réelles.
        intervals = 10**log_intervals  # On revient à l'échelle linéaire avec 10^log.
        
        # Met la valeur maximale à la fin de la liste des intervalles.
        intervals[len(intervals)-1] = max_value

        # Créé des intervalles et compte les valeurs dans chaque intervalle.
        country_level = []
        for i in range(len(intervals) - 1):
            interval1 = intervals[i] # noqa: F841
            interval2 = intervals[i+1] # noqa: F841
            count = df_filtered.query('(CO2_emission >= @interval1) and (CO2_emission <= @interval2)').count()
            country_level.append(count['Country'])         
        
        # Configure l'histogramme.
        fig = px.bar(
            x=[f"{intervals[i]:.2f} - {intervals[i+1]:.2f}" for i in range(len(intervals) - 1)], # Affiche les intervalles sous forme de texte.
            y=country_level,  # Nombre de pays dans chaque intervalle.
            labels={"x": "Intervalle des émissions de CO2", "y": "Nombre de pays"},
            title="Histogramme des émissions de CO2 avec intervalles personnalisés"
        )
        
        # Personnalisation du texte de survol.
        fig.update_layout(
            xaxis_title="Émissions de CO2 (par intervalle)",
            yaxis_title="Nombre de pays",
            paper_bgcolor="#111827", # Couleur de fond.
            font_color="#ffffff" # Couleur du texte.
        )
        
        return fig
import plotly_express as px
import dash
import pandas
import os
import json
from dash import dcc, html
from dash.dependencies import Input, Output
from src.utils import clean_energy_data
from src.components import get_footer, get_header

#
# Data
#
current_dir = os.path.dirname(__file__)  # Directory of the current script

year = 2002

data_path = os.path.join(current_dir, "data/cleaned/formatted_energy.csv")
pop_data = pandas.read_csv(data_path, sep=';')

years = pop_data["Year"].unique()
data = { year:pop_data.query("Year == @year") for year in years}

#
# nos données
#
# Récupération de la colonne 'Code Département' contenant les codes INSEE des communes
countries_code = pop_data['Country']

# Création d'un masque pour ne récupérer que les communes d'IDF
mask = ( ( countries_code.str.startswith('World') ) )

# Filtrage avec le masque pour ne pas prendre = World
pop_data = pop_data[~mask]

energy_type = pop_data['Energy_type']
mask2 = ( ( energy_type.str.startswith('all_energy_types') ) ) # Filtrage avec le masque pour ne pas prendre = all_energy_types
pop_data = pop_data[mask2]

pop_data['ADMIN'] = pop_data.pop('Country')
pop_data["CO2_emission"] = pandas.to_numeric(pop_data["CO2_emission"])

df = pop_data

# Construct the path relative to the script's location

geojson_path = os.path.join(current_dir, "data/cleaned/cleaned_countries.geojson")
with open(geojson_path, "r") as f:
    geojson_data = json.load(f)

#
# Main
#
if __name__ == '__main__':
    #clean_energy_data()

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data[year], x="Energy_consumption", y="Energy_production",
                        color="Country",
                        size="Year",
                        hover_name="Country") # (4)
    
    fig_map = px.choropleth_mapbox(
        df,
        geojson=geojson_data,                           # GeoJSON file
        color="CO2_emission",                      # Column to determine color
        locations="ADMIN",                         # Column in DataFrame with location names
        featureidkey="properties.ADMIN",           # Key in GeoJSON to match `ADMIN`
        color_continuous_scale="YlGn",             # Color scale
        range_color=[0, 15000],                    # Min and max of color scale
        mapbox_style="carto-positron",             # Map style
        zoom=2,                                    # Initial zoom level
        center={"lat": 0, "lon": 0},               # Center of the map
    )


    app.layout = html.Div([
        get_header(years),

        # Title
        html.H1(
            id="title",
            style={'textAlign': 'center', 'color': '#7FDBFF'}
        ),

        # Graphs
        dcc.Graph(
            id='graph1'
        ),

        # Legend
        html.Div(
            id="legend",
            style={'marginTop': '20px'}
        ),

        # Graphs
        dcc.Graph(
            id='graph2',
            figure=fig_map
        ),

        get_footer(),
    ])

    # Callback for interactivity
    @app.callback(
        [Output('graph1', 'figure'),  # Graph
        Output('title', 'children'),  # Title
        Output('legend', 'children')],  # Legend
        [Input('year-slider', 'value')]  # Dropdown input
    )
    def update_dashboard(selected_year):
        """
        Update the graph, title, and legend dynamically based on the selected year.
        """
        # Update the graph
        fig = px.scatter(data[selected_year], 
            x="Energy_consumption", 
            y="Energy_production",
            color="Country",
            size="Year",
            hover_name="Country",
            title=f"Life Expectancy vs GDP per Capita ({selected_year})"
        )

        # Update the title
        title = f"Life Expectancy vs GDP per Capita ({selected_year})"

        # Update the legend
        legend = f"""
        The graph above shows the relationship between life expectancy and GDP per capita for the year {selected_year}. 
        Each continent is represented by a color, and the size of the symbols is proportional to the population of each country. 
        Hover over the points for more details.
        """

        return fig, title, legend
    
    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)
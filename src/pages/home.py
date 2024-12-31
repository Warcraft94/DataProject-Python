from dash import html, dcc
import plotly_express as px
from src.components import create_footer, create_header
#from simple_page import create_default_layout

def create_home_page(years, data, df, geojson_data, year): #TODO: variables en parametres
    fig = px.scatter(data[year], x="Energy_consumption", y="Energy_production",
                        color="Country",
                        size="Year",
                        hover_name="Country")
    
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

    return html.Div([
        create_header(years),

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
            id='graph2'
        ),

        create_footer(),
    ])
import geopandas as gpd
import pandas as pd
import folium
import matplotlib.pyplot as plt
import pickle
from streamlit_folium import folium_static
from folium.plugins import MousePosition
from folium import Choropleth
from folium.features import GeoJsonTooltip

data = gpd.read_file('polygon/Utrecht_NoordHolland.SHP', geometry='geometry') #read the geodataFrame
data = data.to_crs(epsg=4326) # change crs to EPSG:4326
# geodata = data.to_json()
basic_map = folium.Map(location=[52.58709632157862, 4.825269960317581], tiles="openstreetmap", zoom_start=9) #create the folium base map
#Create the choropleth map add it to the base map
custom_scale = (data['inhabitant'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist() # get 20th percentile values for the Choropleth colormap
folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['mzr_name', 'inhabitant'],  #Here we tell folium to get the TAZ name ('mzr_name') and plot population ('inhabitant') metric for each county
            key_on='feature.properties.mzr_name', #Here we grab the geometries boundaries from the geojson file using the key 'mzr_name' 
            threshold_scale=custom_scale, #use the custom scale we created for legend
            fill_color='YlOrRd',
            nan_fill_color="White", #Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='population ', #title of the legend
            highlight=True,
            line_color='black').add_to(basic_map) 
#Add Customized Tooltips to the map
folium.features.GeoJson(
                    data=data,
                    name='population',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['mzr_name',
                                'gem_name',
                                'prov_name',
                                'inhabitant'
                               ],
                        aliases=["TAZ name:",
                                 "Municipality Name:",
                                 "Province Name:",
                                 "population"
                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(basic_map)   

folium_static(basic_map, width=1200, height=800)


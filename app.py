import streamlit as st
from speed import max_speed_df, style_function, colorscale
from kruispunten import df as kruispunten_df
from streamlit_folium import folium_static
import folium

st.set_page_config(layout="wide")

st.title('Dutch Highway Network')

map = folium.Map(
    # location=[51.94, 4.46],
    location=[
        max_speed_df.geometry.to_crs('EPSG:4326').bounds.miny.mean(),
        max_speed_df.geometry.to_crs('EPSG:4326').bounds.minx.mean()
    ],
    zoom_start=10,
    tiles=None
)

base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
# folium.TileLayer(tiles='OpenStreetMap').add_to(base_map)
folium.TileLayer(tiles='cartodbpositron').add_to(base_map)
base_map.add_to(map)

# MAXIMUM SPEED LAYER 
layer_speed = folium.FeatureGroup(name='Speed Limit', overlay=True)
layer_speed.add_to(map)
gjson = folium.GeoJson(
    max_speed_df,
    style_function=style_function,
    popup=['properties'],
).add_to(layer_speed)

folium.features.GeoJsonPopup(
    fields=['WVK_ID', 'BEGAFSTAND', 'ENDAFSTAND', 'OMSCHR'],
    aliases=['WVK_ID', 'from', 'to', 'Maximum speed'],
    labels=True
).add_to(gjson)

# color map
map.add_child(colorscale)

# KRUISPUNTEN LAYER
kruis_layer = folium.FeatureGroup(name='Cross-session', overlay=True)
kruis_layer.add_to(map)

kruis_gjson = folium.GeoJson(
    kruispunten_df,
).add_to(kruis_layer)

folium.features.GeoJsonPopup(
    fields=['OMSCHR', 'RIJRTNGHRB'],
    aliases=['OMSCHR', 'RIJRTNGHRB'],
    labels=True
).add_to(kruis_gjson)


folium.LayerControl().add_to(map)

folium_static(
    map,
    width=900,
    height=900
)
# %%
import geopandas as gpd
import folium
import json

# %%
df = gpd.read_file('data/Kruispunten/kruispunten.shp')

if __name__=="__main__":
    map = folium.Map(
        location=[51.94, 4.46],
        zoom_start=10
    )

    marker_cluster = folium.MarkerCluster().add_to(map)

    gjson = folium.GeoJson(
        df,
    ).add_to(map)

    folium.features.GeoJsonPopup(
        fields=['OMSCHR', 'RIJRTNGHRB'],
        aliases=['OMSCHR', 'RIJRTNGHRB'],
        labels=True
    ).add_to(gjson)

    map
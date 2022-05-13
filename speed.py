import geopandas as gpd
import folium
import json
import branca

# read data
max_speed_df = gpd.read_file('data/Maximum snelheid/max_snelheden.shp')#, rows=10000)
max_speed_df = max_speed_df[['WVK_ID', 'OMSCHR', 'BEGAFSTAND', 'ENDAFSTAND', 'geometry']]
max_speed_df.to_crs('EPSG:4326', inplace=True)
max_speed_df.WVK_ID = max_speed_df.WVK_ID.astype(str)
max_speed_df.head()

geo = gpd.GeoSeries(max_speed_df.set_index('WVK_ID')['geometry']).to_json()
geojson = json.loads(geo)

colorscale = branca.colormap.linear.RdYlBu_11.scale(0, max_speed_df.OMSCHR.max())
def style_function(feature):
    return {
        "fillOpacity": 0.5,
        "weight": 5,
        "color": colorscale(max_speed_df.iloc[int(feature['id'])]['OMSCHR']),
    }

if __name__=="__main__":
    map = folium.Map(
        # location=[51.94, 4.46],
        location=[
            max_speed_df.geometry.to_crs('EPSG:4326').bounds.miny.mean(),
            max_speed_df.geometry.to_crs('EPSG:4326').bounds.minx.mean()
        ],
        zoom_start=10
    )

    gjson = folium.GeoJson(
        # geojson,
        max_speed_df,
        # json.loads(geo),
        style_function=style_function,
        popup=['properties'],
    ).add_to(map)

    folium.features.GeoJsonPopup(
        fields=['WVK_ID', 'BEGAFSTAND', 'ENDAFSTAND', 'OMSCHR'],
        aliases=['WVK_ID', 'from', 'to', 'Maximum speed'],
        labels=True
    ).add_to(gjson)

    map
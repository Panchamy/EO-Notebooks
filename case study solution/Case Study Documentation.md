# Documentation

This file describes the main documentation for the case study solution and provides resources 
for the main packages and functions used.

## Packages
The required packages are described below:
- `Geopandas`: Pandas dataframes optimized for geospatial data, includes geometry variable type
- `Folium`: Visualization package with interactive maps
- `Rasterio`: Package to work with geospatial raster data

## Definitions
Import is to distinguish the different geospatial datatypes. 
In this case study `raster` data, `linestrings` and `polygons` are used.
Raster data is data that is provided for equally sized and distanced
cells and is often continious in form, it can provide an overlay of data.
For example raster data can be temperatures or elevation levels or as in this case 
the risk of flooding. Linestrings are simply just lines drawn from coordinates to coordinates
(they are not necessarly straight and can contain multiple coordinates). Polygons are 
areas that are enclosed by lines, in this case provinces.

See https://shapely.readthedocs.io/ for more information.

## Code
First the geojson file including the provinces and the geojson file including the 
roads within Vietnam are loaded to a geopandas dataframe as _gdf_bound_ and _gdf_road_ respectively. Next to this the raster data
file is loaded as rasterio object.

By using the `rasterio.mask.mask` function it is possible to mask the 
raster data over a certain column with geometry data, in this case the geometry of the boundary
dataframe is used, so the polygons describing the provinces in Vietnam. The plot shows
the raster data masked over the provinces of vietnam.

In code block 5 a more detailed mask is performed on each row separately, in order to plot the 
average flood risk per province. The average value of the mask is calculated and added as column to the row.

These calculated averages can be plot in a simple heatmap.

### Folium plotting
In order to plot provinces and the corresponding flood risk averages first the data needs to be transformed
to a json file. Folium uses this json file as the provided geographical data for the items in the map
(in this case polygons).

Each row of the dataframe is in this json formatted as a feature and each feature includes
an id and geometry. The ID is set by us to be the index of row of the dataframe.
This enables us to add the calculated averages based on the id/index later on.
```
{
"id":"0", 
"type":"Feature", 
"properties":{..}, 
"geometry":
    { "type":"Polygon", 
      "coordinates":[...] }
}
```
First the folium map is instantiated by the folium.Map() function with a start coordinate and zoom level 
(set to see vietnam)
Then the json file is passed to the geo_data argument of the folium.Cholorpleth() function, which will plot
the polygons and matching values with a color scale. The calculated average is included by passing the geopandas 
dataframe gdf_bound. The index column is needed for this plot as the index column is the column
used to join with the json feature id. The average column is the one being plotted as colour scale.

### Vulnerable roads
The same masking function is used for the road data. But in this case a cloropleth element
needs to be added to the folium map for each road line as only polygons can be added as one geo Cloroploth.

### Provinces with vulnerable roads
For the provinces with vulnerable roads question first a weighted average needs to be calculated
to create an average of vulnerable roads per province. The weight is calculated by 
multiplying the road length with the average flood risk per road. 

After this calculation for each road it is identified in which province this road
is located. This join can be done with the `geopandas.sjoin` function.

After this join for each province the average weighted road flood risk is calculated by 
grouping by each province polygon and taking the mean weight (code block 23). 

This mean weight value is then combined again with the original 
province dataframe _gdf_bound_ (see code block 24), in order to add the province name column again.

This data is plotted in the same way as question 1.
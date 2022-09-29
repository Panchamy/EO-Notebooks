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


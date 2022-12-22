#Used to find the difference between two polygons
#Used in jupyter notebook as there is visualisation and interactive map

from geojson import Feature, Polygon, FeatureCollection
from ipyleaflet import Map, GeoJSON, LayersControl
from turfpy.transformation import difference, intersect

aoi_1 = Feature(geometry=Polygon([[
    [13, 52],
    [13, 56],
    [16, 54],
    [15, 52],
    [13, 52]]]), properties={"combine": "yes", "fill": "#00f"})
aoi_2 = Feature(geometry=Polygon([[
    [12, 51],
    [15, 51],
    [15, 55],
    [12, 55],
    [12, 51]]]), properties={"combine": "yes"})


aoi_1_geojson = GeoJSON(name="First Polygon", data=aoi_1)

aoi_2_geojson = GeoJSON(name='Second Polygon', data=aoi_2, style={'color': 'green'})

try:
    aoi_geojson = GeoJSON(name='Difference', data=difference(aoi_1, aoi_2), style={'color': 'red'})
    print("Partial overlap. Difference is remainder AOI. Warning. End results can be multipolygon! \n")
except :
    print("Full overlap, check Intersection \n")
    aoi_geojson = GeoJSON(name='Intersection', data=intersect([aoi_1, aoi_2]), style={'color': 'red'})


print("Resulting AOI polygon:", aoi_geojson,"\n")
m = Map(center=[52, 13], zoom=5)


m.add(aoi_1_geojson)
m.add(aoi_2_geojson)
m.add(aoi_geojson)

control = LayersControl(position='topright')
m.add_control(control)

m
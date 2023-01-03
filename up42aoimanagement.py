import up42
import pandas as pd
from IPython.display import display
from geojson import Feature, Polygon, FeatureCollection
from ipyleaflet import Map, GeoJSON, LayersControl
from turfpy.transformation import difference, intersect
from shapely.geometry import mapping

#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
project = up42.initialize_project()
catalog = up42.initialize_catalog()

#get products available in catalog
products = catalog.get_data_products(basic=True)



# aoi definition
#aoi_example = up42.get_example_aoi()
aoi_1nhalfsqm = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[13.362461,52.524945],[13.381079,52.524945],[13.382023,52.514812],[13.361431,52.514394],[13.362461,52.524945]]]}}]}
aoi_big = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[9.755859,51.808615],[14.040527,53.761702],[16.040039,52.241256],[13.07373,51.124213],[9.755859,51.808615]]]}}]}
aoi_geometry = aoi_big
#print(aoi_geometry)

search_parameters = catalog.construct_search_parameters(collections=["spot"],
                                                        geometry=aoi_geometry,
                                                        start_date="2022-06-01",
                                                        end_date="2022-12-31",
                                                        max_cloudcover=20,
                                                        sortby="cloudCoverage",
                                                        limit=2)

search_results = catalog.search(search_parameters, as_dataframe=False)
#print(search_results)
#used to verify list is empty. Suboptimal to do 2 searches. Refactor
search_results_df = catalog.search(search_parameters, as_dataframe=True)
#print(search_results_df)

if not search_results_df.empty:
    display(pd.DataFrame(search_results_df[["id", "collection", "providerName", "acquisitionDate", "resolution"]]))
else:
    print("\nZERO results for this query. Please adapt your search criteria or look into Tasking. \n")
    exit()


#print(search_results["features"][0]["geometry"]["coordinates"])
#print(search_results.iloc[0]["geometry"]) Used in case dataframe is used


shapely_polygon = search_results_df.iloc[0]["geometry"]
geometry_string = mapping(shapely_polygon)

print(geometry_string)
sr_coordinates = geometry_string["coordinates"]
print(sr_coordinates)

search_results_coordinates = Feature(geometry=Polygon(search_results["features"][1]["geometry"]["coordinates"]))
#print("search results coordinates",search_results_coordinates,"\n")

print("number of search results: ", len(search_results["features"]))

#all_search_results_aoi = FeatureCollection()
#for x in search_results["features"]:
#    all_search_results_aoi = Feature(geometry=Polygon(search_results["features"][x]["geometry"]["coordinates"]))


aoi_1 = aoi_geometry["features"][0]["geometry"]
aoi_1_geojson = GeoJSON(name="AOI Polygon", data=aoi_1)

#aoi_2 = search_results_coordinates
aoi_2 = sr_coordinates
aoi_2_geojson = GeoJSON(name='Search Result Polygon', data=aoi_2, style={'color': 'green'})

try:
    aoi_geojson = GeoJSON(name='Difference/Remaining AOI', data=difference(aoi_1, aoi_2), style={'color': 'red'})
    print("Partial overlap. Difference is remainder AOI. Warning. \n")
    print("End results can be multipolygon OR have holes! \n")
except :
    print("Full overlap, check Intersection \n")
    aoi_geojson = GeoJSON(name='Intersection', data=intersect([aoi_1, aoi_2]), style={'color': 'red'})

#additional serach results beyond the one selected
aoi_3 = Feature(geometry=Polygon(search_results["features"][1]["geometry"]["coordinates"]))
aoi_3_geojson = GeoJSON(name='Search Result Polygon', data=aoi_3, style={'color': 'green'})

#print(aoi_geojson)
m = Map(center=[52, 13], zoom=5)


m.add(aoi_1_geojson)
m.add(aoi_2_geojson)
m.add(aoi_3_geojson)
m.add(aoi_geojson)

control = LayersControl(position='topright')
m.add_control(control)

m


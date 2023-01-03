import up42
import pandas as pd
from IPython.display import display
from shapely.geometry import mapping

#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
project = up42.initialize_project()
catalog = up42.initialize_catalog()

#get products available in catalog
products = catalog.get_data_products(basic=True)


pd.set_option('display.max_columns', None)
#display(pd.DataFrame.from_dict(products))
#display(pd.DataFrame.from_dict(products).transpose())

#display(products)

# aoi definition
#aoi_example = up42.get_example_aoi()
aoi_1nhalfsqm = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[13.362461,52.524945],[13.381079,52.524945],[13.382023,52.514812],[13.361431,52.514394],[13.362461,52.524945]]]}}]}
aoi_geometry = aoi_1nhalfsqm
#print(aoi_geometry)

search_parameters = catalog.construct_search_parameters(collections=["spot"],
                                                        geometry=aoi_geometry,
                                                        start_date="2022-06-01",
                                                        end_date="2022-12-31",
                                                        max_cloudcover=20,
                                                        sortby="cloudCoverage",
                                                        limit=10)

search_results = catalog.search(search_parameters)
print(search_results.iloc[0]["geometry"])


shapely_polygon = search_results.iloc[0]["geometry"]
geometry_string = mapping(shapely_polygon)

print(geometry_string)

#display(pd.DataFrame.from_dict(search_results))
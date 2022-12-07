from pprint import pprint
dimport up42
import pandas as pd
from IPython.display import display


#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
tasking = up42.initialize_tasking()
products = tasking.get_data_products(basic=True)


display(pd.DataFrame(products).transpose())
display(pd.DataFrame(products)["TerraSAR Tasking"]["data_products"])
display(pd.DataFrame(products["TerraSAR Tasking"]))

# aoi definition
#aoi_example = up42.get_example_aoi()
#geometry = up42.read_vector_file("data/aoi_washington.geojson")
aoi_1nhalfsqm = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[13.362461,52.524945],[13.381079,52.524945],[13.382023,52.514812],[13.361431,52.514394],[13.362461,52.524945]]]}}]}
aoi_geometry = aoi_1nhalfsqm
print("aoi defined has been taken into account for the search query.\n")

selected_data_product = "a6f64332-3148-4e05-a475-45a02176f210"

print(tasking.get_data_product_schema(selected_data_product))
pprint(tasking.get_data_product_schema(selected_data_product))

order_parameters = tasking.construct_order_parameters(data_product_id=selected_data_product,
                                                      name="My Terrasar tasking order",
                                                      acquisition_start= "2022-11-01",
                                                      acquisition_end= "2023-03-20",
                                                      geometry=aoi_geometry)


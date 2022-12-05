import pandas as pd
import up42
from IPython.display import display

#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
project = up42.initialize_project()
catalog = up42.initialize_catalog()

#get products available in catalog
products = catalog.get_data_products(basic=True)


pd.set_option('display.max_columns', None)
#display(pd.DataFrame.from_dict(products))
display(pd.DataFrame.from_dict(products).transpose())

display(products)

aoi_geometry = up42.get_example_aoi()

search_parameters = catalog.construct_search_parameters(collections=["spot"],
                                                        geometry=aoi_geometry,
                                                        start_date="2022-06-01",
                                                        end_date="2022-12-31",
                                                        max_cloudcover=20,
                                                        sortby="cloudCoverage",
                                                        limit=10)

search_results = catalog.search(search_parameters)

display(pd.DataFrame.from_dict(search_results))


data_product_id = "acc3f9a4-b622-49c1-b1e1-c762aa3e7e13"
image_id = search_results.iloc[0]["id"]
order_parameters = catalog.construct_order_parameters(data_product_id=data_product_id,
                                                      image_id=image_id,
                                                      aoi=aoi_geometry)
display(order_parameters)

catalog.estimate_order(order_parameters)

acceptance = input("enter yes or no to order")
if acceptance == "yes":
    order = catalog.place_order(order_parameters)
else:
    print("not ordered")

print("End of script")
#print(disp[0])
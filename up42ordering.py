import up42
import pandas as pd
from IPython.display import display


#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
project = up42.initialize_project()
catalog = up42.initialize_catalog()

#get products available in catalog
products = catalog.get_data_products(basic=True)



#display(pd.DataFrame.from_dict(products))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)
display(pd.DataFrame.from_dict(products).transpose())

#add error handling for wrong input

try:
    selected_providername = input("\nPlease type the provider name you are interested in: \n")
    selected_collection = products[selected_providername]["collection"]
    print("Selected Provider: ", selected_providername, "\nSelected collection:", selected_collection)
except KeyError:
    print("Wrong entry. Please check wording. ")


display(pd.DataFrame(products[selected_providername]))

selected_dataproduct = input("\nEnter the id of the data_product you are interested in: \n")
#display(pd.DataFrame(products[select_name]['data_products']))


# aoi definition
#aoi_example = up42.get_example_aoi()
aoi_1nhalfsqm = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[13.362461,52.524945],[13.381079,52.524945],[13.382023,52.514812],[13.361431,52.514394],[13.362461,52.524945]]]}}]}
aoi_geometry = aoi_1nhalfsqm
print("aoi defined has been taken into account for the search query.\n")

search_parameters = catalog.construct_search_parameters(collections=[selected_collection],
                                                        geometry=aoi_geometry,
                                                        start_date="2022-06-01",
                                                        end_date="2022-12-31",
                                                        max_cloudcover=20,
                                                        sortby="cloudCoverage",
                                                        limit=10)

search_results = catalog.search(search_parameters)
if not search_results.empty:
    display(pd.DataFrame(search_results[["id","collection","providerName","acquisitionDate","resolution"]]))
else:
    print("\nZERO results for this query. Please adapt your search criteria or look into Tasking. \n")
    exit()

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 150)
# display(pd.DataFrame.from_dict(search_results))


data_product_id = selected_dataproduct
search_results_index = int(input("\nPlease enter the search result index you are interested in purchasing: "))
image_id = search_results.iloc[search_results_index]["id"]
order_parameters = catalog.construct_order_parameters(data_product_id=data_product_id,
                                                      image_id=image_id,
                                                      aoi=aoi_geometry)
estimate = catalog.estimate_order(order_parameters)

print("Credit estimate for this purchase is: ",estimate," credits")

acceptance = input("enter yes or no to order")

if acceptance == "yes":
    order = catalog.place_order(order_parameters)
else:
    print("not ordered")

print("End of script")

import up42
import pandas as pd
from IPython.display import display

#Authentication & initialisation
up42.authenticate(cfg_file="../secret/config.json")
project = up42.initialize_project()

#get workflows/jobs, storage and assets lists
workflow = project.get_jobs()
storage = up42.initialize_storage()
assets = storage.get_assets(limit=100, sortby="size", descending=False)


# displayTable function to display tables using panda
def displayTable(inputList, param1, param2, param3, param4, param5, message):
    list = []
    for x in inputList:
        list.append([x.info[param1],x.info[param2],x.info[param3],x.info[param4],x.info[param5]])
    df=pd.DataFrame(data=list, columns=[param1, param2, param3, param4, param5])
    print(message)
    display(df)

displayTable(workflow, "displayId", "status", "updatedAt", "name", "createdAt", "Jobs run by user")
displayTable(assets,"name", "source", "createdAt","size","orderId", "Available Assets in Storage")

#print(assets)

#assets[0].download()
#assets[0].results

#print(assets[3].info)
#print(assets[0].info,sep="\n") #display available info about Assets object

#workflow[5].download_quicklooks()
#workflow[5].map_quicklooks() #I get an error there
#up42.draw_aoi()

#workflow[3].download_results()
#workflow[3].map_results()
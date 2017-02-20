import pymongo
from exophase import Exophase
from datetime import datetime
import json

if __name__ == "__main__":

    url = "https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn"

    connection = pymongo.MongoClient("localhost", 27017)
    db = connection['gamedb']
    collection = db.achievement

    exo = Exophase()

    #searchResult = exo.search("wrc 6")
    # print(searchResult)

    url = "https://www.exophase.com/game/wrc-6-ps4/"

    items = collection.find({"gid": exo.getId(url)})

    if items.count() == 0:
        collection.insert(exo.getInfo(url))
        print("insert")
    else:
        print("already inserted")




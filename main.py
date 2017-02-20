import pymongo
from exophase import Exophase
from datetime import datetime
import json

if __name__ == "__main__":

    url = "https://www.exophase.com/game/fifa-17-ps4/"

    connection = pymongo.MongoClient("localhost", 27017)
    db = connection['gamedb']
    collection = db.achievement

    exo = Exophase()

    items = collection.find({"_id": exo.getId(url)})

    if items.count() == 0:
        collection.insert(exo.getInfo(url))
        print("insert")
    else:
        print("already inserted")



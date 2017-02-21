import pymongo
from exophase import Exophase
from datetime import datetime
import json
import os

if __name__ == "__main__":

    db = "sogeuni.iptime.org"
    url = "https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn"

    connection = pymongo.MongoClient(db, 27017)
    db = connection['gamedb']
    collection = db.achievement

    imgPath = os.getcwd() + "/img"

    exo = Exophase(imgPath=imgPath)

    #searchResult = exo.search("wrc 6")
    # print(searchResult)

    # url = "https://www.exophase.com/game/wrc-6-ps4/"
    # url = "https://www.exophase.com/game/wrc-6-steam/"
    # url = "https://www.exophase.com/game/the-inner-world-xbox-one/"
    url = "https://www.exophase.com/game/wrc-6-fia-world-rally-championship-xbox-one/"

    items = collection.find({"gid": exo.getId(url)})

    if items.count() == 0:
        collection.insert(exo.getInfo(url))
        print("insert")
    else:
        print("already inserted")




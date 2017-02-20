from urllib.parse import quote_plus, urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

logging.basicConfig(level=logging.DEBUG)

class Exophase:
    def __init__(self, url="https://www.exophase.com"):
        logging.debug("Exophase init: " + url)
        self.__url = urlparse(url)
        self.BASE_URL = self.__url.geturl()
        self.SEARCH_URL = self.BASE_URL + "/search?s="
        self.LINK_CHECKER = self.__url.netloc + "/game/"
        self.PUBLISHER_CHECKER = self.__url.netloc + "/publisher/"
        self.DEVELOPER_CHECKER = self.__url.netloc + "/developer/"
        self.GENRE_CHECKER = self.__url.netloc + "/genre/"

        logging.debug("BASE_URL: " + self.BASE_URL)
        logging.debug("SEARCH_URL: " + self.SEARCH_URL)

    def getUpdateList(self):
        logging.debug("getUpdateList()")

        if self.__url.scheme == "file":
            url = self.BASE_URL + "index.html"
        else:
            url = self.BASE_URL

        return self.__getLinks(url)

    def search(self, title):
        logging.debug("search: " + title)
        url = self.SEARCH_URL + quote_plus(title)
        logging.debug("search url: " + url)
        return self.__getLinks(url)

    def __getLinks(self, url):
        html = urlopen(url)
        bs = BeautifulSoup(html, "lxml")
        links = bs.findAll("a", href=re.compile(self.LINK_CHECKER))

        for i in range(len(links)):
            links[i] = links[i]['href']

        return list(set(links))

    def __getPsInfo(self, url, debug=False):
        if debug == False:
            url += (url[len(url)-1] == "/") and "trophies/kr/" or "/trophies/kr/"

        logging.debug("getInfo changed_url: " + url)

        html = urlopen(url)
        bs = BeautifulSoup(html, "lxml")

        items = bs.findAll("li", {"data-type":"trophy"})

        results = []

        for item in items:
            result = {}
            result["id"] = item["data-award-id"]
            result["secret"] = False if (item.find("div", {"class": "secret"}) == None) else True
            result["title"] = item.find("div", {"class": "trophy-title"}).get_text().strip()
            result["desc"] = item.find("div", {"class": "trophy-desc"}).get_text().strip()
            result["type"] = item.find("div", {"class": "type"}).span['title'].lower()

            # Bronze - 15
            # Silver - 30
            # Gold - 90
            # Platinum - 180
            if result["type"] == "platinum":
                result["score"] = 180
            elif result["type"] == "gold":
                result["score"] = 90
            elif result["type"] == "silver":
                result["score"] = 30
            else:
                result["score"] = 15

            result["rarity"] = item.find("div", {"class": "rarity"}).span.span['title'].lower()

            results.append(result)

        return results

    def __getXboxInfo(self, url, debug=False):
        if debug == False:
            url += (url[len(url) - 1] == "/") and "achievements/kr/" or "/achievements/kr/"

        logging.debug("getInfo changed_url: " + url)

        html = urlopen(url)
        bs = BeautifulSoup(html, "lxml")

        items = bs.findAll("li", {"data-type":"achievement"})

        results = []

        for item in items:
            result = {}
            result["id"] = item["data-award-id"]
            result["secret"] = False if (item.find("div", {"class": "secret"}) == None) else True
            result["title"] = item.find("div", {"class": "trophy-title"}).get_text().strip()
            result["desc"] = item.find("div", {"class": "trophy-desc"}).get_text().strip()
            result["type"] = None
            result["score"] = int(re.findall(r'\d+', item.find("div", {"class": "gamerscore"}).get_text())[0])
            result["rarity"] = item.find("div", {"class": "rarity"}).span.span['title'].lower()

            results.append(result)

        return results

    def __getGameInfo(self, url, result):
        html = urlopen(url)
        bs = BeautifulSoup(html, "lxml")

        result["title"] = bs.find("div", {"class":"info-top-block"}).h2.get_text().strip()
        result["platform"] = [item.get_text().lower() for item in \
                              bs.find("div", {"class":"info-top-block"}).findAll("div", {"class":"inline-pf"})]
        try:
            result["publisher"] = bs.find("a", href=re.compile(self.PUBLISHER_CHECKER)).get_text().strip()
        except:
            result["publisher"] = ""

        try:
            result["developer"] = bs.find("a", href=re.compile(self.DEVELOPER_CHECKER)).get_text().strip()
        except:
            result["developer"] = ""

        try:
            result["genre"] = [item.get_text().lower() for item in bs.findAll("a", href=re.compile(self.GENRE_CHECKER))]
        except:
            result["genre"] = ""

        try:
            result["release"] = datetime.strptime(bs.find("dt", text="Release Date:")
                                                .findNext().get_text().strip(), "%B %d, %Y").strftime("%Y-%m-%d")
        except:
            result["release"] = ""


    def getInfo(self, url, debug=False):
        logging.debug("getInfo: " + url)

        result = {}

        result['gid'] = self.getId(url)

        self.__getGameInfo(url, result)

        if "ps3" in url or "ps4" in url or "psn" in url:
            result['type'] = "trophy"
            items = self.__getPsInfo(url, debug)
        else:
            result['type'] = "achievement"
            items = self.__getXboxInfo(url, debug)

        result['total-score'] = sum(item['score'] for item in items)
        result['item-count'] = len(items)
        result['items'] = items
        logging.debug(result)

        return result

    def getId(self, url):
        import hashlib

        logging.debug("getId: " + url)

        l = [x for x in url.split("/") if x]
        return hashlib.md5(l[len(l) - 1].encode("utf-8")).hexdigest()

if __name__ == "__main__":
    import random
    import datetime

    # random.seed(datetime.datetime.now())

    # exo = Exophase("file:///Volumes/Data/personal/exo/")
    exo = Exophase()
    # links = exo.getUpdateList()
    # links = exo.search("prominence poker")

    # for link in links:
    #     print(link)

    # print(exo.getInfo("file:///Volumes/Data/personal/exo/fifa-17-ps4.html", debug=True))
    # print(exo.getInfo("file:///Volumes/Data/personal/exo/test.html", debug=True))
    # print(exo.getInfo("https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn"))
    exo.getInfo("https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn/")

    # import hashlib
    # print(hashlib.md5(b"https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn").hexdigest())
    # print(hashlib.md5(b"https://www.exophase.com/game/super-robot-wars-og-the-moon-dwellers-psn/").hexdigest())

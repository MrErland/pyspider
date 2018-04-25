from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re


def getlinks(articleUrl):
    try:
        html = urlopen("http://en.wikipedia.org"+articleUrl)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
    except AttributeError as e:
        return None
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

if __name__ == '__main__':
	random.seed(datetime.datetime.now())
	links = getlinks("/wiki/linux")
	while len(links) > 0:
   		newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
   		print(newArticle)
   		links = getlinks(newArticle)


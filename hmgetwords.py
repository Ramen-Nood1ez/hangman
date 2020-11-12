from bs4 import BeautifulSoup
import urllib.request
import re


def getwords():
    url = "https://Ramen-Nood1ez.github.io/hangman/index.html"
    uf = urllib.request.urlopen(url)
    html = uf.read()
    var = re.sub("b*'", "", str(html))
    var = re.split('"*"', string=var)
    print(var)
    return var[1]

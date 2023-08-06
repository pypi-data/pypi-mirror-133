import requests
from bs4 import BeautifulSoup

def checkConnection():
    URL= "https://karanshah7371.github.io/Trigger/"

    page=requests.get(URL)

    soup =BeautifulSoup(page.content, "html.parser")

    results= soup.find(id="flag")

    if results.text == "1":
        return True

    else:
        return False

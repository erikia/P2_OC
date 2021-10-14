import requests
from bs4 import BeautifulSoup
import os

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


def getdata(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


categories = []


def get_book_data(soup):
    """Fonction pour analyser les données d'un livre"""
    print("Démarrage du scrapping")

    tds = soup.find_all(["td"])

    title = soup.find("h1")
    print(title.text)

    upc = tds[0]
    print(upc.text)

    price_excluding_tax = tds[2]
    print(price_excluding_tax.text)

    price_including_tax = tds[3]
    print(price_including_tax.text)

    number_available = tds[5]
    print(number_available.text)

    description = soup.find("article").find_all(
        "p")[3].get_text().replace(";", "/").strip()
    print(description)

    category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2]
    print(category.text)

    rating = soup.find(
        "div", {"class": "col-sm-6 product_main"}).find_all("p")[2]["class"][1]
    print(rating)

    images = soup.find('img')
    name_img = images['alt']
    link_img = images['src']
    print(name_img, link_img)

    print("Opération terminé")


get_book_data(soup)

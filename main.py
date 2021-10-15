from typing import Text
import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from pathlib import Path


"""url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

"""


def getdata(url):
    """Fonction pour se connecter au site """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_categories_data(url_categories):
    """Fonction pour récupérer l'ensemble des catégories"""
    url = getdata("https://books.toscrape.com/index.html")
    list_categories = []
    if getdata.status_code == requests.codes.ok:
    ul_cat = url.find_all("div", class_="side_categories").ul.ul
    a_cat = url.find("a")
       for cat in side_categories.find_all('a')["href"][1:]:
            get_categories_data.append('https://books.toscrape.com/')
        return get_categories_data
    print(get_categories_data)



def get_url_books(pages_parse):
    """Fonction pour récupérer l'ensemble des livres"""
    return


def get_book_data(soup):
    """Fonction pour analyser les données d'un livre"""
    print("Démarrage du scrapping")
    page = BeautifulSoup(soup.content, "html.parser")
    tds = soup.find_all(["td"])
    title = soup.find("h1")
    upc = tds[0]
    price_excluding_tax = tds[2]
    price_including_tax = tds[3]
    number_available = tds[5]
    description = soup.find("article").find_all(
        "p")[3].get_text().replace(";", "/").strip()
    category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2]
    rating = soup.find(
        "div", {"class": "col-sm-6 product_main"}).find_all("p")[2]["class"][1]
    images = soup.find('img')['src']
    product_list = {
        'title': title.text,
        'category': category.text,
        'description': description,
        'rating': rating,
        'price_et': price_excluding_tax.text,
        'price_it': price_including_tax.text,
        'upc': upc.text,
        'stock': number_available.text,
        'img': images,
        'url': page, }
    print("Opération terminé")



get_book_data(soup)

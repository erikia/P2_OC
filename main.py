import requests
from bs4 import BeautifulSoup
import os

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


def getdata(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_book_data(soup):
    """Fonction pour analyser les données d'un livre"""
    print("Démarrage du scrapping")

    title = soup.find("h1").get_text()
    print(title)

    upc = soup.find_all("td")[0].get_text()
    print(upc)

    price_excluding_tax = soup.find_all("td")[2].get_text()
    print(price_excluding_tax)

    price_including_tax = soup.find_all("td")[3].get_text()
    print(price_including_tax)

    number_available = soup.find_all("td")[5].get_text()
    print(number_available)

    description = soup.find("article").find_all(
        "p")[3].get_text().replace(";", "/").strip()
    print(description)

    category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2].text
    print(category)

    rating = soup.find(
        "div", {"class": "col-sm-6 product_main"}).find_all("p")[2]["class"][1]
    print(rating)

    for item in soup.find_all("img"):
        name_img = item['alt']
        link_img = item['src']
        print(name_img, link_img)

    print("Opération terminé")


get_book_data(soup)

"test"

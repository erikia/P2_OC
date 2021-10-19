import requests
from bs4 import BeautifulSoup
import csv
from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin


main_url = 'http://books.toscrape.com/'
book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


def getdata(url):
    """Fonction pour se connecter au site """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_categories_data(url_categories):
    """Fonction pour récupérer l'ensemble des catégories"""
    soup = getdata(url)
    list_categories = []
    if soup.status_code == requests.codes.ok:
        ul_cat = soup.find_all("div", class_="side_categories").ul.ul
        for cat in ul_cat.find_all('a')["href"][1:]:
            list_categories.append('https://books.toscrape.com/')
        return list_categories
    print(list_categories)


def get_url_books(list_categories):
    """Fonction pour récupérer l'ensemble des livres"""
    list_book = []
    category_urls = []
    soup = getdata(url)
    for book_list in list_categories:
        if soup.status_code == requests.codes.ok:
            category_urls.append(book_list)
            for div in soup.select('h3', 'a')["href"]:
                list_book.append('https://books.toscrape.com/catalogue/')
        # pagination
        while True:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")

            footer_element = soup.select_one('li.current')
            print(footer_element.text.strip())

            next_page_element = soup.select_one('li.next > a')
            if next_page_element:
                next_page_url = next_page_element.get('href')
                url = urljoin(url, next_page_url)
            else:
                break
    return list_book


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
        'product_page_url': page,
        'title': title.text,
        'upc': upc.text,
        'price_including_tax': price_including_tax.text,
        'price_excluding_tax': price_excluding_tax.text,
        'number_available': number_available.text,
        'review_rating': rating,
        'product_description': description,
        'category': category.text,
        'url_image': images,
    }
    return product_list


print("Opération terminé")


def convert_csv(filesdata):
    """Fonction pour convertir le ficher en csv"""
    with open("data.csv", "w") as csvfile:
        data_names = [
            'product_page_url',
            'title',
            'upc',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'review_rating',
            'product_description',
            'category',
            'url_image',
        ]
        writer = cvs.DictWriter(csvfile, delimiter='|', filenames=data_names)
        writer.writeheader()
        for data in filesdata:
            writer.writerow(data)
    print(filesdata)


def img_download():
    """requests.get()
    urllib.requests.urlopen()
    enregistrere directement au format binaire  en mode écriture binaire
    """
    f = open('', 'wb')
    response = requests.get('https://books.toscrape.com/catalogue/')
    f.write(response.content)
    f.close()

    print("download successful")

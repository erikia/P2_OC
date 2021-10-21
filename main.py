import requests
from bs4 import BeautifulSoup
import csv
from csv import DictWriter
from pathlib import Path


url = ("http://books.toscrape.com/")
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"


def getdata(url):
    """Fonction pour se connecter au site """
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        print("Page erreur")
        return False


def get_categories_urls(url_categories):
    """Fonction pour récupérer l'ensemble des urls des catégories-x"""
    soup = getdata(url_categories)
    category_next_urls = []
    list_categories = []
    for _ in url_categories:
        if soup.status_code == requests.codes.ok:
            category_next_urls.append(_)
        for div in soup.select('h3 a'):
            list_categories.append(
                'https://books.toscrape.com/catalogue/' + (div.get('href')[9:]))
    return list_categories


def get_url_books(url):
    """Fonction pour récupérer l'ensemble des urls des  livres-x"""
    list_categories = get_categories_urls(url)
    urls_books = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_books = soup.find_all("article", "product_pod")

    category = soup.find("h1").get_text()

    for i in soup_books:
        url_book = i.a["href"].replace("../", "")
        urls_books.append(url_book)

    next_page = soup.find("li", "next")
    url = url.replace("index.html", "")
    while next_page:
        url_next_page = url + next_page.a["href"]
        request = requests.get(url_next_page)
        html = request.content
        soup = BeautifulSoup(html, features="html.parser")
        soup_books = soup.find_all("article", "product_pod")
        for i in soup_books:
            url_book = i.a["href"].replace("../", "")
            urls_books.append(url_book)
        next_page = soup.find("li", "next")

    return urls_books, category


def get_book_data(soup):
    """Fonction pour analyser les données d'un livre"""
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


def export_csv(filesdata):
    """Fonction pour exporter le ficher en csv"""
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
        writer = csv.DictWriter(csvfile, delimiter='|', filenames=data_names)
        writer.writeheader()
        for data in filesdata:
            writer.writerow(data)
    print(filesdata)


def main():
    f = get_url_books(url)
    print(f)


"""     "Fonction principale"
    url = "http://books.toscrape.com"
    urls_category = get_categories_urls(url)
    for url_category in urls_category:
        books = []
        url = f"http://books.toscrape.com/{url_category}"
        print(url)
        urls_book, category = get_url_books(url)
        for url_book in urls_book:
            url_book = f"http://books.toscrape.com/catalogue/{url_book}"
            book = get_book_data(url_book)
            book.category = category
            books.append(book)
        export_csv(books, category)
        break """


if __name__ == '__main__':
    main()

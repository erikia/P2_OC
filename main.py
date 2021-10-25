import requests
from bs4 import BeautifulSoup
import csv
from csv import DictWriter
from pathlib import Path


#url = ("http://books.toscrape.com/")
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"


def category_url(url_first):
    page = requests.get(url_first)
    if page.status_code == requests.codes.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        side_categories = soup.find('div', class_='side_categories')
        category_urls = []
        for _ in side_categories.find_all('a')[1:]:
            category_urls.append('https://books.toscrape.com/' + _.get('href'))
        return category_urls


def category_urls_next(category_urls, urls_books):
    """Fonction pour récupérer l'ensemble des urls des  livres"""
    urls_books = []
    request = requests.get(category_urls)
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
    print(urls_books, category)
    return urls_books, category


def get_book_data(soup):
    """Fonction pour analyser les données d'un livre"""
    soup = BeautifulSoup(soup.content, "html.parser")
    page = category_urls_next(urls_books)
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
    print(product_list)
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
    url = 'https://books.toscrape.com/index.html'
    a = category_url(url)
    b = category_urls_next(a)
    c = get_book_data(b)
    print(c)


if __name__ == '__main__':
    main()

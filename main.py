
import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from slugify import slugify
import urllib
from urllib.parse import urljoin


URL_BASE = "http://books.toscrape.com/"
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"
category_mystery_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


def get_soup(url):
    """Fonction pour appeler et analyser une page Web HTML """
    request = requests.get(url)
    if not request.ok:
        print("Obtenu une page d'erreur")
        return None
    return BeautifulSoup(request.content, 'html.parser')


def get_category_urls(categories_url: list[str]) -> list:
    """Retourne les liens de chaque catégories"""
    categories_url = []
    categories = get_soup(URL_BASE).find_all('ul')[
        2].find_all('li')

    for category in categories:
        # Récupération des urls des pages de chaque catégorie
        # category_url = URL_BASE + category.find('a')['href']
        # categories_url_replace = category_url.replace("index.html", " ")
        categorys = category.find('a')['href']
        category_url = urllib.parse.urljoin(URL_BASE, categorys)
        categories_url.append(category_url)
    # print(categories_url)
    return categories_url


def get_book_urls_from_categories(page_url: str) -> list:
    book_urls = []

    next_button = True
    page = 1
    while next_button:
        if page == 1:
            url = page_url
        else:
            url = page_url.replace("index.html", f"page-{page}.html")

        page += 1
        soup = get_soup(url)
        h3_balise = soup.find_all('h3')

        for h3 in h3_balise:
            books_urls = h3.a['href']
            link_url = urllib.parse.urljoin(url, books_urls)
            book_urls.append(link_url)

        next_button = soup.find('li', class_='next')
        print(len(book_urls))
    return book_urls


def get_book_data(url) -> dict:
    """Retourne les données demandées pour chaque livre"""
    soup = get_soup(url)
    category = soup.find_all('li')[2]
    tds = soup.find_all(["td"])
    upc = tds[0].text
    universal_product_code = tds[0].text
    title = (soup.find('h1').text)
    price_including_tax = tds[3].text
    price_excluding_tax = tds[2].text
    number_available = tds[5].text
    product_description = soup.find(
        'div', id='product_description')
    if product_description is None:
        product_description = 'No description'
    else:
        product_description = product_description.find_next_sibling(
            "p").text
    review_rating = soup.find("p", class_="star-rating")
    replace_title = slugify(soup.find('h1').text)

    product_list = {
        'product_page_url': url,
        'title': title,
        'upc': upc,
        'universal_product_code': universal_product_code,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'review_rating': review_rating['class'][1],
        'product_description': product_description,
        'category': category.a.text,
        'url_image': URL_BASE + soup.img['src'][6:],
        'img_file': f"{IMG_DIR}/{slugify(category.a.text)}/{replace_title}.jpg",
    }
    return product_list


def save_images(file, image):
    """Sauvegarder une image"""
    with open(f'{file}', 'wb') as f:
        f.write(image)


def save_book_data_to_csv(books_data):
    """Sauvegarde les données des livres dans un fichier csv"""
    category = slugify(books_data[0].get('category'))
    header = books_data.keys()
    # header = ["product_page_url","universal_ product_code (upc)","title" ,"price_including_tax","price_excluding_tax" ,"number_available","product_description","category","review_rating","image_url"]
    with open(f'{CSV_DIR}{category}.csv', 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, filedsnames=header, dialect='excel')
        writer.writeheader()
        writer.writerows(books_data)


def main():
    "Fonction principale"
    Path(CSV_DIR).mkdir(parents=True, exist_ok=True)
    print('Récupération des urls des catégories en cours ...')
    category_urls = get_category_urls(URL_BASE)
    print('Récupération des urls des livres en cours ...')

    for category_url in category_urls:
        print(f'Traitement de la catégorie {category_url} en cours ...')
        books_data = []
        book_urls = get_book_urls_from_categories(category_url)

        for book_url in book_urls:
            book_data = get_book_data(book_url)
            books_data.append(book_data)

        img_url = []
        images_files = []
        for book in book_data:
            print(f'Traitement des livres {len(book)} en cours ...')
            img_url.append(book[0].get('img_url'))
            image_file = (
                f"{IMG_DIR}{slugify(book.get('category'))}/"
                f"{slugify(book.get('title'))}.jpg"
            )
            images_files.append(image_file)

        images = []
        category = book_data[0].get('category')
        Path(f'{IMG_DIR + category}').mkdir(parents=True, exist_ok=True)
        for image in images:
            print(f'Traitement des images {image} en cours ...')
            image = save_images(image)

        save_book_data_to_csv(book_data)
        return book_data


if __name__ == "__main__":
    main()
    # #categories = get_category_urls(URL_BASE)
    # books_urls = get_book_urls_from_categories(category_mystery_url)
    # print(books_urls)

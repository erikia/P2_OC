import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from slugify import slugify
import urllib


URL_BASE = "http://books.toscrape.com/"
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"
star_rating = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}


def get_soup(url):
    """Retourne le contenu d'une page Web HTML"""
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
        category_href = category.find('a')['href']
        category_url = urllib.parse.urljoin(URL_BASE, category_href)
        categories_url.append(category_url)
    return categories_url


def get_book_urls_from_categories(page_url: str) -> list:
    """Retourne les liens des livres pour chaque catégories"""
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

    return book_urls


def get_book_data(url) -> dict:
    """Retourne les données demandées pour chaque livre"""
    soup = get_soup(url)
    category = soup.find_all('li')[2]
    tds = soup.find_all(["td"])
    upc = tds[0].text
    title = (soup.find('h1').text)
    price_including_tax = tds[3].text
    price_excluding_tax = tds[2].text
    available = tds[5].text
    number_available = int(''.join(filter(str.isdigit, available)))
    url_image = URL_BASE + soup.img['src']
    product_description = soup.find(
        'div', id='product_description')
    if product_description is None:
        product_description = 'No description'
    else:
        product_description = product_description.find_next_sibling(
            "p").text
    review_rating = star_rating[soup.find(
        class_="star-rating")['class'][1]]
    replace_title = slugify(soup.find('h1').text)

    product_list = {
        'product_page_url': url,
        'title': title,
        'upc': upc,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'review_rating': review_rating,
        'product_description': product_description,
        'category': category.a.text,
        'url_image': url_image,
        'img_file': f"{IMG_DIR}/{slugify(category.a.text)}/{replace_title}.jpg",
    }
    return product_list


def save_images(content, filename):
    """Sauvegarder une image"""
    with open(f'{filename}', 'wb') as f:
        f.write(content)


def save_book_data_to_csv(books_data):
    """Sauvegarde les données des livres dans un fichier csv"""
    category = slugify(books_data[0].get('category'))
    header = books_data[0].keys()
    with open(f'{CSV_DIR}{category}.csv', 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=header, dialect='excel')
        writer.writeheader()
        writer.writerows(books_data)


def main():
    """Fonction principale"""
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

        for book in books_data:
            booktitle = slugify(book.get('title'))
            print(f'Traitement du livre {booktitle} en cours ...')
            url_image = book.get('url_image', {})
            category = slugify(books_data[0].get('category'))
            image_file = (
                f"{IMG_DIR + category}/"
                f"{slugify(book.get('title'))}.jpg"
            )
            Path(f'{IMG_DIR + category}').mkdir(parents=True, exist_ok=True)
            response = requests.get(url_image)
            save_images(response.content, image_file)

            save_book_data_to_csv(books_data)


if __name__ == "__main__":
    main()

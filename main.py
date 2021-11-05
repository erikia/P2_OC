import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from slugify import slugify

URL_BASE = "http://books.toscrape.com/"
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"


def get_soup(url):
    """Fonction pour appeler et analyser une page Web HTML """
    url = "http://books.toscrape.com/"
    request = requests.get(url)
    if not request.ok:
        print("Obtenu une page d'erreur")
        return None
    return BeautifulSoup(request.content, 'html.parser')


def get_category_urls(categories_url):
    """Fonction pour récupérer les liens de chaque catégories"""
    categories_url = []
    categories = get_soup(URL_BASE).find_all('ul')[
        2].find_all('li')

    for category in categories:
        # Récupération des urls des pages de chaque catégorie
        category_url = URL_BASE + category.find('a')['href']
        categories_url = category_url.split(',')
    return categories_url


def get_book_urls_from_categories(categories_url):
    """Fonction pour récupérer les liens des livres à partir des catégories"""
    book_urls = []
    category_url = get_category_urls(categories_url)
    next_botton = get_soup(category_url).find('li', class_='next')
    while next_botton:
        page = slugify(category_url) + (next_botton.find('a')['href'])
        next_botton = get_soup(page).find('li', class_='next')
        categories_url.append(page)
        continue
        break
    # Récupération des urls des livres des pages de chaque catégorie
    for page in categories_url:
        books = get_soup(page).find_all(
            'div', class_="image_container")
        for book in books:
            book = slugify(
                ('https://books.toscrape.com/catalogue/' + book.find('a')['href']))
            book_urls.append(book)
        return book_urls


def get_book_data(url):
    # Obtenir les données demandées pour chaque livre
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
    """Fonction pour sauvegarder une image"""
    with open(f'{file}', 'wb') as f:
        f.write(image)


def save_book_data_to_csv(books_data):
    """Fonction pour sauvegarder les données des livres dans un fichier csv"""
    category = slugify(books_data[0].get('category'))
    header = books_data[0].keys()
    with open(f'{CSV_DIR}{category}.csv', 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, filedsnames=header, dialect='excel')
        writer.writeheader()
        writer.writerows(books_data)


def main():
    "Fonction principale"
    Path(CSV_DIR).mkdir(parents=True, exist_ok=True)

    category_urls = get_category_urls(URL_BASE)
    for category_url in category_urls:
        book_data = []
        book_urls = get_book_urls_from_categories(category_url)

        for book_url in book_urls:
            book_data = get_book_data(book_url)
            book_data.append(book_data)

        images = []
        function = []
        images_files = []
        for book in book_data:
            function.append(book.get('img_url'))
            image_file = (
                f"{IMG_DIR}{slugify(book.get('category'))}/"
                f"{slugify(book.get('title'))}.jpg"
            )
            images_files.append(image_file)

        category = book_data[0].get('category')
        Path(f'{IMG_DIR + category}').mkdir(parents=True, exist_ok=True)
        for image in images:
            image = save_images(image)

        save_book_data_to_csv(book_data)
        return book_data


if __name__ == "__main__":
    main()

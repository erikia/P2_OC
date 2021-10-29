import requests
from bs4 import BeautifulSoup
import csv
from csv import DictWriter
from pathlib import Path
import os


url = ("http://books.toscrape.com/")
IMG_DIR = "data/img/"
CSV_DIR = "data/csv/"


def get_soup(url):
    """Fonction pour se connecter au site """
    url = "http://books.toscrape.com/"
    request = requests.get(url)
    if not request.ok:
        print("Obtenu une page d'erreur")
        return None
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup


def replace_text(txt, special_characters):
    for special_character in special_characters:
        return(txt.replace(special_character, ''))

def get_data_books(book):
    soup = get_soup(book)
    return(soup.find_all('td'))

def get_category_urls(url_first):
    """Fonction pour appeler et analyser une page Web HTML"""
    soup = get_soup(url_first)
    side_categories = soup.find('div', class_='side_categories')
    category_urls = []
    for i in side_categories.find_all('a')[1:]:
        category_urls.append('https://books.toscrape.com/' + i.get('href'))
    return category_urls


def get_books_urls(category_urls):
    """Fonction pour récupérer les liens de chaque catégories"""
    books_urls = []
    url = 'http://books.toscrape.com/'
    category_urls = get_soup(url).find_all('ul')[2].find_all('li')

    for category_url in category_urls:
        soup = get_soup(category_url)
        categorie_name = category.find('a').text.strip(' \n\t')
        path = categorie_name
        if not os.path.exists(categorie_name):
            os.mkdir(categorie_name)

        # Création d'un fichier csv avec les en-tête pour chaque catégorie dans les répertoires catégorie correspondant
        with open(os.path.join(path, f'{categorie_name}.csv'), 'w', encoding='utf-8-sig') as file:
            headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                   'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            file.write(';'.join(headers) + '\n')



        category = url + category_url.find('a')['href']
        books_urls = category.split(',')
        next_botton = get_soup(category).find('li', class_='next')
        while next_botton:
            page = category.replace(
            'index.html', '')+(next_botton.find('a')['href'])
            next_botton = get_soup(page).find('li', class_='next')
            books_urls.append(page)
            continue
            break

        for page in books_urls:
            books = get_soup(page).find_all(
            'div', class_="image_container")
            for book in books:
                book_url = replace_text(
                ('https://books.toscrape.com/catalogue/' + book.find('a')['href']), special_characters)

                # Obtenir les données demandées pour chaque livre
                soup = get_soup(book_url)
                data = get_data_books(book_url)
                product_page_url = book_url
                universal_product_code = data[0].text
                title = replace_text((soup.find('h1').text), '/"-')
                price_including_tax = data[3].text
                price_excluding_tax = data[2].text
                number_available = data[5].text

                 # Ajouter dans fichiers csv crées précédemment les données de chaque livre
                with open(os.path.join(path, f'{categorie_name}.csv'), 'a', encoding='utf-8-sig') as file:
                    file.write(';'.join(valeurs) + '\n')

            # télécharger les images dans répertoire de chaque catégorie
                with open(os.path.join(path, f'{title}.jpg'), 'ab') as file:
                    image = requests.get(image_url).content
                    file.write(image)

    


a = get_category_urls(url)
get_books_urls(a)

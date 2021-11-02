import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

url_base = "http://books.toscrape.com/"
special_characters = ['../', ';', ":", '?', '#', '/', ')', '(', '']
star_rating = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}
Path = os.path.abspath(os.getcwd())


def get_soup(url):
    """Fonction pour appeler et analyser une page Web HTML """
    response = requests.get(url)
    if not response.ok:
        print("Obtenu une page d'erreur")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    return(soup)


def replace_special_characters(txt, special_characters):
    """Fonction pour remplacer les caractères spéciaux"""
    for special_character in special_characters:
        return(txt.replace(special_character, ''))


def categories_url():
    categories_url = []
    # Récupération des liens de chaque catégorie:
    categories = get_soup(url_base).find_all('ul')[2].find_all('li')

    for category in categories_url(categories):
        # Création d'un dossier pour chaque catégorie
        categorie_name = category.find('a').text.strip(' \n\t')

        for category_url in categories_url():
            category_soup = get_soup(url=category_url)
            categorie_name = category_soup.find('strong').text
            path = categorie_name

            if not os.path.exists(categorie_name):

                os.mkdir(categorie_name)
                file = Path(path, f'{categorie_name}.csv')
                file.open('a').write(';'.join(headers)+'\n')

            divs_book = category_soup.find_all('div', class_="image_container")

            for div_book in divs_book:

                book_url = 'https://books.toscrape.com/catalogue/' + \
                    div_book.find('a')['href']
                book_url = urljoin(
                    'https://books.toscrape.com/catalogue', book_url)
                soup = get_soup(book_url)

                product_list = soup.find_all('td')

                file.open(
                    'a', encoding='utf-8-sig').write(';'.join(product_list)+'\n')

                image = requests.get(product_list[9]).content
                fileb = Path(path, f'{product_list[2]}.jpg')
                fileb.open('wb').write(image)

            # Création d'un fichier csv avec les en-tête pour chaque catégorie dans les répertoires catégorie correspondant
            with open(os.path.join(path, f'{categorie_name}.csv'), 'w', encoding='utf-8-sig') as file:
                headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                           'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                file.write(';'.join(headers) + '\n')

            # Récupération des urls des pages de chaque catégorie
            category_url = url_base + category.find('a')['href']
            categories_url = category_url.split(',')
            next_botton = get_soup(category_url).find('li', class_='next')
            while next_botton:
                page = category_url.replace(
                    'index.html', '')+(next_botton.find('a')['href'])
                next_botton = get_soup(page).find('li', class_='next')
                categories_url.append(page)
                continue
                break

            # Récupération des urls des livres des pages de chaque catégorie
            for page in categories_url:
                books = get_soup(page).find_all(
                    'div', class_="image_container")
                for book in books:
                    book_url = 'https://books.toscrape.com/catalogue/' + \
                        book.find('a')['href']
                    book_url = urljoin(
                        'https://books.toscrape.com/catalogue', book_url)

                    # Obtenir les données demandées pour chaque livre
                    soup = get_soup(book_url)
                    data = soup.find_all('td')
                    product_page_url = book_url
                    universal_product_code = data[0].text
                    title = replace_special_characters(
                        (soup.find('h1').text), '/"-')
                    price_including_tax = data[3].text
                    price_excluding_tax = data[2].text
                    number_available = data[5].text

                    # Recherche si description livre et remplacer certains caractères
                    product_description = soup.find(
                        'div', id='product_description')
                    if product_description is None:
                        product_description = 'No description'
                    else:
                        product_description = replace_special_characters(
                            (soup.find_all('p')[3].text), special_characters[1])

                    # Rechercher la note de cahque livre et la transformer en chiffre
                    review_rating = star_rating[soup.find(
                        class_="star-rating")['class'][1]]

                    image_url = replace_special_characters(
                        (url_base + soup.find('img')['src']), special_characters)

                    product_list = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                                    number_available, product_description, categorie_name, review_rating, image_url]

                    # Ajouter dans fichiers csv crées précédemment les données de chaque livre
                    with open(os.path.join(path, f'{categorie_name}.csv'), 'a', encoding='utf-8-sig') as file:
                        file.write(';'.join(product_list) + '\n')

                    # télécharger les images dans répertoire de chaque catégorie
                    with open(os.path.join(path, f'{title}.jpg'), 'ab') as file:
                        image = requests.get(image_url).content
                        file.write(image)

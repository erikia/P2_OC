# P2_OC
Projet 2 : Utilisez les bases de Python pour l'analyse de marché

Ce projet a pour but de créer un script Python pour scrapper le site : https://books.toscrape.com/index.html. 
Le script crée un fichier CSV pour chaque livres de chaques catégories et un dossier conetenant les images des livres.
    
# Processus
## Catégories
Le script fait une requête sur le site books.toscrape.com. Si la requête est accessible, le script récupérer toutes les 50 catégories puis crée ensuite une liste pour les répertorier. Par la suite, le script va pouvoir créer un fichier CSV par catégorie où nous allons récupérer chacun des livres dans leurs dossiers respectifs.
De plus, le script va récupérer pour chaque catégorie toutes les pages selon la quantité de livres.

## Livres
Nous allons ensuite placer les liens des livres dans un dictionnaire qui procède ensuite au scrapping de toutes les données que nous placerons voir dans un fichier csv pour chaque page de livres.

Dans ce fichier csv, il sera classé avec ces données :

* url
* title
* upc
* price_including_tax
* price_excluding_tax
* number_available
* review_rating
* product_description
* category
* url_image
* img_file

## Images
Pour chaque fois, livre, le script va télécharger l'image du livre en un fichier ".jpg" correspondant dans le dossier "img".
Ensuite, il écrit pour chaque livres dans le fichier csv de la catégorie qui porte son nom dans le dossier "csv".

# Utilisation

## Création de l'environnement virtuel

Pour la mise en palce de l'environnement virtuel :

## Sur Windows :
Dans le Windows Powershell il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P2_OC.git

### Activer l'environnement virtuel
    $ cd P2_OC 
    $ python -m venv env 
    $ ~env\scripts\activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
    $ python main.py
    
----------------------------------------------
## Sur MacOS ou Linux :
Dans le terminal, il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P2_OC.git

### Activer l'environnement virtuel
    $ cd P2_OC 
    $ python3 -m venv env 
    $ source env/bin/activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
    $ python3 main.py

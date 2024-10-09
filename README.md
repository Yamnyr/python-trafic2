# Python-Trafic

## Description

**Python-Trafic** est un projet de Data Analysis centré sur l'analyse de données de trafic. Ce projet permet d'effectuer des requêtes et analyses de données soit à partir de fichiers locaux avec **Pandas**, soit directement sur une base de données **SQLite**. 

## Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- [Anaconda](https://www.anaconda.com/products/distribution) (comme interpréteur Python)
- Python 3.x (inclus dans Anaconda)
- Les bibliothèques Python suivantes (gérées via Anaconda ou pip) :
  - pandas
  - sqlite3
  - jupyter
  - matplotlib
  - seaborn
  - numpy
  - dotenv
  - os

## Installation

1. Clonez le projet en local :

    ```bash
    git clone https://github.com/Yamnyr/python-trafic2
    cd python-trafic2
    ```

2. Installez les dépendances Python nécessaires :

    ```bash
    conda install pandas sqlite jupyter matplotlib seaborn numpy python-dotenv

    ```

3. Configurez les accès aux fichiers de données dans le fichier `.env` :

    - Ouvrez le fichier `.env`.
    - Modifiez les chemins d'accès vers les fichiers de données selon votre environnement local.

5. Lancez le script `config.py` pour installer et remplir la base de données SQLite :

## Utilisation

### Exécuter des requêtes avec Pandas

Pour analyser les données à partir de fichiers locaux avec **Pandas** :

1. Ouvrez le fichier `requete_panda.ipynb` dans Jupyter Notebook :

2. Exécutez les cellules du notebook pour analyser les fichiers.

### Exécuter des requêtes SQL sur la base de données SQLite

Pour analyser les données à partir de la base de données **SQLite** :

1. Ouvrez le fichier `requete_sql.ipynb` dans Jupyter Notebook :

2. Exécutez les cellules du notebook pour interagir avec la base de données et faire des requêtes SQL.
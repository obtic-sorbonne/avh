#!/bin/bash
# Prépare un environnement Python et installe les dépendances nécessaires

# Crée un environnement virtuel (nommé venv)
python3 -m venv avh_env

# Active l'environnement
source avh_env/bin/activate

# Met à jour pip
pip install --upgrade pip

# Installe les dépendances externes
pip install beautifulsoup4 lxml markdown
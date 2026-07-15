# mastermind/__init__.py
"""
Ce module de package définit l'API publique du package Mastermind.
Il expose les classes de jeu et les utilitaires via __all__ pour faciliter les imports.
"""

# Import des classes de base et variantes de jeu
from .mastermind_game import MastermindGame  # Classe abstraite principale
from .variants import StandardGame, BeginnersGame  # Variantes Standard et for Beginners

# Import des fonctions utilitaires pour la génération et le filtrage de codes
from .utils import (
    generate_secret,       # Génération d'un code secret aléatoire
    all_possible_codes,    # Construction de tous les codes possibles
    filter_possible_codes, # Filtrage selon le feedback obtenu
    random_guess           # Sélection aléatoire d'une proposition
)

# Déclaration de l'API publique du package
# Seules les entités listées ici seront importées lorsqu'on utilise:
#   from mastermind import *
__all__ = [
    "MastermindGame",       # Classe abstraite de base
    "StandardGame",         # Variante classique du jeu
    "BeginnersGame",        # Variante pour débutant
    "generate_secret",      # Fonction utilitaire de génération de code
    "all_possible_codes",   # Fonction utilitaire pour toutes les combinaisons
    "filter_possible_codes",# Fonction pour filtrer les codes possibles
    "random_guess",         # Fonction pour sélectionner une proposition aléatoire
]

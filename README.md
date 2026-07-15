# Mastermind Simulator

Application web (Flask) qui simule des parties de Mastermind résolues automatiquement par un codebreaker, et qui analyse statistiquement le nombre de tentatives nécessaires sur un grand nombre de simulations.

## Contexte

Projet réalisé à deux (Anis Mokhtari & Aymeric Pedanou) dans le cadre du cours *Object-Oriented Programming in Python* (M1 MAEF, Université Paris 1 Panthéon-Sorbonne, 2025). Le sujet imposait plusieurs contraintes : une architecture strictement orientée objet (abstraction et héritage), une implémentation vectorisée avec NumPy, l'usage des seules bibliothèques standard `numpy` et `flask`, et une structure de projet imposée.

Le sujet complet est inclus dans le dépôt (`sujet.pdf`).

## Fonctionnalités

- **Quatre variantes de jeu**, obtenues en combinant deux règles alternatives :
  - Mode **Standard** (feedback global : nombre de pions bien placés / mal placés) et mode **Beginners** (feedback positionnel : chaque position reçoit `red`, `white` ou `none`), implémentés via une classe abstraite `MastermindGame` et deux sous-classes (`StandardGame`, `BeginnersGame`).
  - Répétition des couleurs **autorisée ou interdite** dans le code secret.
- **Résolution automatique** : conformément au sujet, le codebreaker utilise une stratégie simple — à chaque tour, il propose un code tiré aléatoirement parmi ceux encore cohérents avec l'ensemble des feedbacks obtenus. L'espace des candidats est filtré après chaque proposition jusqu'à trouver le code secret.
- **Simulation à grande échelle** : lance N parties (codes secrets tirés uniformément) et calcule la moyenne, l'écart-type et le maximum du nombre de tentatives, ainsi que la distribution complète.
- **Interface web Flask** : formulaire de configuration (nombre de couleurs, longueur du code, répétition, mode de jeu, nombre de simulations) et page de résultats affichant les statistiques et un histogramme de la distribution.

## Structure du projet

```
.
├── app.py                     # Serveur Flask : routes et boucle de simulation
├── mastermind/                # Package Python
│   ├── __init__.py            # API publique du package
│   ├── mastermind_game.py     # Classe abstraite MastermindGame
│   ├── variants.py            # StandardGame, BeginnersGame
│   └── utils.py               # Génération de codes, calcul du feedback, filtrage
├── templates/
│   ├── index.html             # Formulaire de configuration
│   └── results.html           # Page de résultats (stats + histogramme)
├── static/                    # CSS et images
├── mastermindenv.yml          # Environnement Conda (Linux/Windows)
├── mastermindenv_mac.yml      # Environnement Conda (macOS)
├── sujet.pdf                  # Énoncé du projet
└── knuth-mastermind.pdf       # Référence : l'article original de Knuth sur Mastermind
```

## Installation et lancement

Avec Conda (recommandé, comme demandé dans le sujet) :

```bash
conda env create -f mastermindenv.yml      # ou mastermindenv_mac.yml sur macOS
conda activate mastermindenv
python app.py
```

Alternativement, avec pip :

```bash
python -m venv venv
source venv/bin/activate                   # Windows : venv\Scripts\activate
pip install flask numpy
python app.py
```

Ouvrir ensuite l'adresse affichée dans le terminal (par défaut `http://127.0.0.1:5000`).

## Note sur l'algorithme

La stratégie du codebreaker est volontairement simple (tirage aléatoire parmi les candidats cohérents), car c'est celle imposée par l'énoncé. L'article de Knuth fourni en référence (`knuth-mastermind.pdf`) décrit une stratégie plus fine (minimax) qui garantit une résolution en au plus 5 coups au Mastermind classique ; elle n'est pas utilisée ici, l'objectif du projet étant l'architecture orientée objet et l'analyse statistique plutôt que l'optimisation du solveur.

## Auteurs

Anis Mokhtari & Aymeric Pedanou

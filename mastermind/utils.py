import numpy as np
import itertools
import random
from typing import List, Tuple, Dict


def generate_secret(
    n_colors: int,
    code_length: int,
    allow_repetition: bool = True
) -> np.ndarray:
    """
    Génère un code secret aléatoire pour le jeu Mastermind.

    :param n_colors: nombre total de couleurs disponibles (numérotées de 0 à n_colors-1)
    :param code_length: longueur du code secret à générer
    :param allow_repetition: si True, les couleurs peuvent se répéter dans le code
    :return: numpy.ndarray de taille (code_length,) contenant le code secret
    """
    if allow_repetition:
        # Génère un tableau d'entiers aléatoires, chaque entier représentant une couleur
        return np.random.randint(0, n_colors, size=code_length)
    else:
        # Choisit un échantillon sans répétition dans la gamme de couleurs
        return np.array(random.sample(range(n_colors), code_length))


def all_possible_codes(
    n_colors: int,
    code_length: int,
    allow_repetition: bool = True
) -> List[Tuple[int, ...]]:
    """
    Construit toutes les combinaisons possibles de codes selon les paramètres.

    :param n_colors: nombre total de couleurs (0 à n_colors-1)
    :param code_length: longueur des codes à générer
    :param allow_repetition: si True, les codes peuvent contenir des répétitions de couleurs
    :return: liste de tuples (chaque tuple est un code possible)
    """
    if allow_repetition:
        # Produit cartésien : toutes les combinaisons avec répétition
        return list(itertools.product(range(n_colors), repeat=code_length))
    else:
        # Permutations : toutes les combinaisons sans répétition
        return list(itertools.permutations(range(n_colors), code_length))


def compute_feedback(
    secret: Tuple[int, ...],
    guess: Tuple[int, ...],
    n_colors: int
) -> Dict[str, int]:
    """
    Calcule le feedback entre le code secret et la proposition.
    Le feedback comporte deux valeurs :
      - 'red'  : nombre de pions de bonne couleur et bonne position
      - 'white': nombre de pions de bonne couleur mais mauvaise position

    :param secret: tuple représentant le code secret
    :param guess: tuple représentant la proposition du joueur
    :param n_colors: nombre total de couleurs
    :return: dictionnaire {'red': int, 'white': int}
    """
    # Conversion en array numpy pour opérations vectorielles
    secret_arr = np.array(secret)
    guess_arr = np.array(guess)

    # 'red' : positions exactes correspondantes
    red = int(np.sum(secret_arr == guess_arr))

    # Comptage de chaque couleur dans secret et guess
    sec_counts = np.bincount(secret_arr, minlength=n_colors)
    gue_counts = np.bincount(guess_arr, minlength=n_colors)

    # 'total' : nombre total de pions de bonne couleur (inclut both red and white)
    total = int(np.sum(np.minimum(sec_counts, gue_counts)))

    # 'white' = total sans les rouges déjà comptés
    white = total - red

    return {'red': red, 'white': white}


def filter_possible_codes(
    possible_codes: List[Tuple[int, ...]],
    guess: Tuple[int, ...],
    feedback: Dict[str, int],
    n_colors: int
) -> List[Tuple[int, ...]]:
    """
    Filtre la liste des codes possibles en ne gardant que ceux compatibles
    avec le feedback obtenu pour la proposition donnée.

    :param possible_codes: liste initiale de codes candidats
    :param guess: tuple de la proposition effectuée
    :param feedback: feedback attendu sous forme {'red': x, 'white': y}
    :param n_colors: nombre de couleurs
    :return: nouvelle liste de codes restants après filtrage
    """
    filtered: List[Tuple[int, ...]] = []
    # Pour chaque code, on calcule le feedback et on compare
    for code in possible_codes:
        fb = compute_feedback(code, guess, n_colors)
        if fb == feedback:
            filtered.append(code)
    return filtered


def random_guess(
    possible_codes: List[Tuple[int, ...]]
) -> Tuple[int, ...]:
    """
    Sélectionne au hasard une proposition parmi les codes possibles.

    :param possible_codes: liste de codes candidats
    :return: un code choisi aléatoirement
    """
    return random.choice(possible_codes)

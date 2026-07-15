from abc import ABC, abstractmethod
import numpy as np


class MastermindGame(ABC):
    """
    Classe abstraite représentant une partie de Mastermind.
    Définit l'interface commune pour générer un code secret et calculer le feedback.
    """

    def __init__(self,
                 n_colors: int,
                 code_length: int,
                 allow_repetition: bool = True):
        """
        Initialise une partie de Mastermind.

        :param n_colors: nombre de couleurs disponibles (les couleurs sont représentées par des entiers de 0 à n_colors-1)
        :param code_length: longueur du code secret à deviner
        :param allow_repetition: si True, la même couleur peut apparaître plusieurs fois dans le code secret
        """
        # Nombre total de couleurs
        self.n_colors = n_colors
        # Nombre de positions dans le code secret
        self.code_length = code_length
        # Indique si les couleurs peuvent se répéter dans le code secret
        self.allow_repetition = allow_repetition
        # Génère et stocke le code secret sous forme d'un tableau numpy
        self._secret = self.generate_code()

    @abstractmethod
    def generate_code(self) -> np.ndarray:
        """
        Génère un nouveau code secret.

        Doit être implémenté par chaque variante de jeu (par exemple Standard, Beginner, etc.).

        :return: un numpy.ndarray de taille (code_length,) contenant les couleurs du code secret
        """
        ...  # À implémenter dans la classe fille

    @abstractmethod
    def compute_feedback(self, guess: np.ndarray) -> dict:
        """
        Calcule le feedback pour une proposition ("guess").

        Le feedback se compose de deux valeurs :
        - 'red'  : nombre de pions bien placés (bonne couleur, bonne position)
        - 'white': nombre de pions de la bonne couleur mais mal placés

        :param guess: un numpy.ndarray de taille (code_length,) représentant la proposition du joueur
        :return: dictionnaire {'red': int, 'white': int}
        """
        ...  # À implémenter dans la classe fille

    def reset(self):
        """
        Réinitialise la partie en générant un nouveau code secret.
        Utile pour lancer à nouveau une simulation ou une nouvelle partie.
        """
        # Appelle generate_code() pour remplacer l'ancien code secret
        self._secret = self.generate_code()

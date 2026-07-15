# mastermind/variants.py
import numpy as np
from .mastermind_game import MastermindGame
from .utils import generate_secret


class StandardGame(MastermindGame):
    """
    Variante classique de Mastermind.
    Feedback en deux valeurs :
      - 'red'  : bonnes couleurs aux bonnes positions
      - 'white': bonnes couleurs aux mauvaises positions
    """
    def __init__(
        self,
        n_colors: int = 6,
        code_length: int = 4,
        allow_repetition: bool = True
    ):
        """
        Initialise la partie Standard.

        :param n_colors: nombre de couleurs disponibles
        :param code_length: longueur du code secret
        :param allow_repetition: indique si les couleurs peuvent se répéter
        """
        super().__init__(n_colors, code_length, allow_repetition)

    def generate_code(self) -> np.ndarray:
        """
        Génère le code secret en utilisant la fonction utilitaire generate_secret.

        :return: numpy.ndarray de taille (code_length,)
        """
        return generate_secret(
            self.n_colors,
            self.code_length,
            self.allow_repetition
        )

    def compute_feedback(self, guess: np.ndarray) -> dict:
        """
        Calcule le feedback pour une proposition.

        Étapes :
        1. 'red' : nombre de pions dont la couleur et la position sont correctes.
        2. Compte total des pions de bonne couleur (roges + blancs).
        3. 'white' = total - red.

        :param guess: numpy.ndarray de taille (code_length,) représentant la proposition
        :return: dict {'red': int, 'white': int}
        """
        # 1. Compter les rouges (match exact position-couleur)
        red = int(np.sum(self._secret == guess))

        # 2. Comptage par couleur dans secret et guess
        secret_counts = np.bincount(
            self._secret,
            minlength=self.n_colors
        )
        guess_counts = np.bincount(
            guess,
            minlength=self.n_colors
        )

        # 3. Nombre total de matching colors (rouges + blancs)
        total_matches = int(
            np.sum(
                np.minimum(secret_counts, guess_counts)
            )
        )

        # 4. Blancs = matches totaux moins rouges déjà comptés
        white = total_matches - red

        return {"red": red, "white": white}


class BeginnersGame(MastermindGame):
    """
    Variante débutant : feedback positionnel sous forme de liste.
    Chaque position reçoit :
      - 'red'  : couleur et position correctes
      - 'white': couleur correcte, position incorrecte
      - 'none' : couleur absente du code secret
    """
    def __init__(
        self,
        n_colors: int = 6,
        code_length: int = 4,
        allow_repetition: bool = True
    ):
        """
        Initialise la partie Beginners.

        :param n_colors: nombre de couleurs disponibles
        :param code_length: longueur du code secret
        :param allow_repetition: indique si les couleurs peuvent se répéter
        """
        super().__init__(n_colors, code_length, allow_repetition)

    def generate_code(self) -> np.ndarray:
        """
        Génère le code secret en utilisant la fonction utilitaire generate_secret.

        :return: numpy.ndarray de taille (code_length,)
        """
        return generate_secret(
            self.n_colors,
            self.code_length,
            self.allow_repetition
        )

    def compute_feedback(self, guess: np.ndarray) -> list:
        """
        Calcule le feedback positionnel pour chaque pion proposé.

        Méthode :
        1. Première passe : identifier et marquer tous les 'reds'.
        2. Deuxième passe : pour chaque position non-validée :
           - si la couleur est encore présente dans le code, c'est un 'white';
           - sinon, c'est un 'none'.

        :param guess: numpy.ndarray de taille (code_length,)
        :return: liste de chaînes ('red', 'white', 'none') de longueur code_length
        """
        feedback = []
        # Copie mutable du secret pour marquer les couleurs déjà attribuées
        secret_copy = list(self._secret.copy())

        # 1. Identification des rouges
        for i, color_guess in enumerate(guess):
            if color_guess == self._secret[i]:
                feedback.append('red')  # bonne couleur & position
                secret_copy[i] = None  # retirer cette couleur du pool
            else:
                feedback.append(None)  # placeholder temporaire

        # 2. Identification des blancs et none
        for i, color_guess in enumerate(guess):
            if feedback[i] is None:
                if color_guess in secret_copy:
                    feedback[i] = 'white'  # bonne couleur, mauvaise position
                    # retirer une occurrence de cette couleur
                    secret_copy[secret_copy.index(color_guess)] = None
                else:
                    feedback[i] = 'none'  # couleur non présente

        return feedback

from flask import Flask, render_template, request, url_for
import numpy as np
from collections import Counter
from mastermind.variants import StandardGame, BeginnersGame
from mastermind.utils import all_possible_codes, filter_possible_codes, random_guess


# Création de l'application Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Route pour afficher la page d'accueil contenant le formulaire de simulation.
    Méthode HTTP : GET
    """
    return render_template('index.html')


@app.route('/simulate', methods=['POST'])
def simulate():
    """
    Route pour lancer la simulation Mastermind.
    Méthode HTTP : POST

    Récupère les paramètres du formulaire, exécute n_simulations parties
    et calcule les statistiques et la distribution des nombres de tentatives.

    Retourne la page results.html avec les données de simulation.
    """
    # ------------------------- Lecture des paramètres -------------------------
    # Nombre de couleurs sélectionné par l'utilisateur
    n_colors = int(request.form['n_colors'])
    # Longueur du code secret
    code_length = int(request.form['code_length'])
    # Autorise ou non la répétition de couleurs dans le code
    allow_repetition = request.form.get('allow_repetition') == 'on'
    # Mode de jeu : 'standard' ou 'beginner'
    mode = request.form['mode']
    # Nombre total de simulations à effectuer
    n_sim = int(request.form['n_simulations'])

    # Liste pour stocker le nombre de tentatives de chaque simulation
    attempts_list = []

    # ----------------------- Boucle de simulation -----------------------------
    for _ in range(n_sim):
        # Initialisation du jeu selon le mode choisi
        if mode == 'standard':
            game = StandardGame(
                n_colors=n_colors,
                code_length=code_length,
                allow_repetition=allow_repetition
            )
        else:
            game = BeginnersGame(
                n_colors=n_colors,
                code_length=code_length,
                allow_repetition=allow_repetition
            )

        # Génération de tous les codes possibles (espace de recherche)
        possible_codes = all_possible_codes(
            n_colors,
            code_length,
            allow_repetition
        )

        attempts = 0  # Compteur de tentatives pour cette partie

        # Boucle de résolution automatique
        while True:
            # Choix aléatoire d'une proposition parmi les codes possibles
            guess = random_guess(possible_codes)
            attempts += 1

            # Calcul du feedback pour la proposition
            feedback = game.compute_feedback(np.array(guess))

            # Vérification de la condition de victoire selon le mode
            if mode == 'standard' and feedback['red'] == code_length:
                break  # Toutes les positions sont correctes
            if mode == 'beginner' and all(p == 'red' for p in feedback):
                break  # Tous les pions sont rouges

            # Filtrage de l'espace de recherche selon le feedback obtenu
            if mode == 'standard':
                possible_codes = filter_possible_codes(
                    possible_codes,
                    guess,
                    feedback,
                    n_colors
                )
            else:
                # Variante beginner : recalculer en instanciant temporairement chaque code
                new_codes = []
                for code in possible_codes:
                    temp_game = BeginnersGame(
                        n_colors,
                        code_length,
                        allow_repetition
                    )
                    temp_game._secret = np.array(code)  # on force le secret
                    if temp_game.compute_feedback(np.array(guess)) == feedback:
                        new_codes.append(code)
                possible_codes = new_codes

        # Stockage du nombre de tentatives pour cette simulation
        attempts_list.append(attempts)

    # ----------------------- Calcul des statistiques -------------------------
    avg_attempts = round(float(np.mean(attempts_list)),2)      # Moyenne des tentatives  round(..., 2) pour arrondir à 2 chiffres significatifs
    std_attempts = round(float(np.std(attempts_list)),2)       # Écart-type
    max_attempts = int(np.max(attempts_list))         # Tentatives maximales

    # Construction de la distribution des tentatives
    dist_counter = Counter(attempts_list)
    distribution = sorted(dist_counter.items())       # Liste de (tentative, fréquence)
    max_freq = max(freq for _, freq in distribution)  # Fréquence max pour l'histogramme

    # ----------------------- Rendu du template -------------------------------
    return render_template(
        'results.html',
        avg=avg_attempts,
        std=std_attempts,
        max_attempts=max_attempts,
        n_sim=n_sim,
        distribution=distribution,
        max_freq=max_freq
    )


if __name__ == '__main__':
    # Démarrage du serveur en mode debug pour le développement
    app.run(debug=True)

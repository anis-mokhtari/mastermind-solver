# Mastermind Simulator

A Flask web application that automatically solves games of Mastermind and statistically analyzes the number of attempts required across a large number of simulations.

## Context

Project developed for the *Object-Oriented Programming in Python* course (M1 MAEF, Université Paris 1 Panthéon-Sorbonne, 2025). The assignment enforced several constraints: a strictly object-oriented architecture (abstraction and inheritance), NumPy-based vectorization, using only the standard `numpy` and `flask` libraries, and a predefined project structure.

The full assignment brief is included in the repository (`sujet.pdf`).

## Features

- **Four game variants**, obtained by combining two alternative rules:
  - **Standard** mode (global feedback: number of correctly and incorrectly placed pegs) and **Beginners** mode (position-wise feedback: each position gets `red`, `white` or `none`), implemented through an abstract `MastermindGame` class and two subclasses (`StandardGame`, `BeginnersGame`).
  - Color repetition in the secret code **allowed or forbidden**.
- **Automatic solving**: as specified in the assignment, the codebreaker uses a simple strategy — at each turn it proposes a code drawn at random among those still consistent with all previous feedback. The candidate space is filtered after each guess until the secret code is found.
- **Large-scale simulation**: runs N games (secret codes drawn uniformly) and computes the mean, standard deviation and maximum number of attempts, along with the full distribution.
- **Flask web interface**: a configuration form (number of colors, code length, repetition, game mode, number of simulations) and a results page displaying the statistics and a histogram of the distribution.

## Project structure

```
.
├── app.py                     # Flask server: routes and simulation loop
├── mastermind/                # Python package
│   ├── __init__.py            # Public API of the package
│   ├── mastermind_game.py     # Abstract class MastermindGame
│   ├── variants.py            # StandardGame, BeginnersGame
│   └── utils.py               # Code generation, feedback computation, filtering
├── templates/
│   ├── index.html             # Configuration form
│   └── results.html           # Results page (stats + histogram)
├── static/                    # CSS and images
├── mastermindenv.yml          # Conda environment (Linux/Windows)
├── mastermindenv_mac.yml      # Conda environment (macOS)
├── sujet.pdf                  # Assignment brief
└── knuth-mastermind.pdf       # Reference: Knuth's original paper on Mastermind
```

## Installation and usage

With Conda (recommended, as required by the assignment):

```bash
conda env create -f mastermindenv.yml      # or mastermindenv_mac.yml on macOS
conda activate mastermindenv
python app.py
```

Alternatively, with pip:

```bash
python -m venv venv
source venv/bin/activate                   # Windows: venv\Scripts\activate
pip install flask numpy
python app.py
```

Then open the address shown in the terminal (default: `http://127.0.0.1:5000`).

## A note on the algorithm

The codebreaker's strategy is intentionally simple (random choice among consistent candidates), as this is the strategy required by the assignment. The Knuth paper included as a reference (`knuth-mastermind.pdf`) describes a more sophisticated minimax strategy that guarantees solving classic Mastermind in at most 5 moves; it is not used here, as the goal of the project was the object-oriented design and statistical analysis rather than solver optimization.

## Author

Anis Mokhtari

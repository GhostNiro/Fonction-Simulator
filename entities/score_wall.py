#on utilise la fonction carrée mais elle sera remplacée plus tard par la formule saisie par l'utilisateur
def square(x):
    return x ** 2


class ScoreWall:
    """Mur du bas : porte le capital de points à détruire.

    x = nombre d'impacts cumulés sur ce mur depuis le début de la partie.
    À chaque impact, formula(x) points sont retirés (jamais sous 0).
    """

    def __init__(self, points, formula=square):
        self.points = points
        self.formula = formula
        self.bounces = 0

    def hit(self):
        self.bounces += 1
        self.points = max(0, self.points - self.formula(self.bounces))
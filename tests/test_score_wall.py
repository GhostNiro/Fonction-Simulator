from config.settings import MAX_WALL_POINTS
from entities.arena import Arena
from entities.ball import Ball
from entities.score_wall import ScoreWall
from physics.collisions import bounce_bottom


def test_wall_starts_with_chosen_points():
    wall = ScoreWall(100)
    assert wall.points == 100


def test_wall_keeps_maximum_value_exactly():
    wall = ScoreWall(MAX_WALL_POINTS)
    assert wall.points == 10**12


def test_hit_subtracts_formula_of_bounce_count():
    wall = ScoreWall(100)  # formule par défaut : x²
    wall.hit()
    assert wall.points == 99  # x = 1


def test_hits_are_cumulative():
    wall = ScoreWall(100)
    for _ in range(3):
        wall.hit()
    assert wall.bounces == 3
    assert wall.points == 100 - 1 - 4 - 9


def test_points_never_go_below_zero():
    wall = ScoreWall(10)
    for _ in range(3):  # 10 - 1 - 4 - 9 -> clampé à 0
        wall.hit()
    assert wall.points == 0


def test_custom_formula_is_used():
    wall = ScoreWall(100, formula=lambda x: 10)
    wall.hit()
    assert wall.points == 90


def test_one_impact_removes_points_only_once():
    arena = Arena(20, 20, 460, 660)
    wall = ScoreWall(100)
    ball = Ball(100, 675, 10, vy=100)

    for _ in range(2):  # frame d'impact, puis frame suivante (balle qui remonte)
        if bounce_bottom(ball, arena):
            wall.hit()

    assert wall.bounces == 1
    assert wall.points == 99
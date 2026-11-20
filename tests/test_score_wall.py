from config.settings import MAX_WALL_POINTS
from entities.score_wall import ScoreWall


def test_wall_starts_with_chosen_points():
    wall = ScoreWall(100)
    assert wall.points == 100


def test_wall_keeps_maximum_value_exactly():
    wall = ScoreWall(MAX_WALL_POINTS)
    assert wall.points == 10**12
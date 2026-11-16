from entities.arena import Arena
from entities.ball import Ball
from physics.collisions import bounce_top

ARENA = Arena(20, 20, 460, 660)  # mur du haut à y = 20


def test_bounce_top_reverses_vertical_speed():
    ball = Ball(100, 25, 10, vx=30, vy=-100)  # bord haut à 15, dans le mur
    bounce_top(ball, ARENA)
    assert ball.vy == 100
    assert ball.vx == 30


def test_bounce_top_puts_ball_back_inside():
    ball = Ball(100, 25, 10, vy=-100)
    bounce_top(ball, ARENA)
    assert ball.y == 30  # arena.top + radius


def test_no_bounce_when_not_touching():
    ball = Ball(100, 200, 10, vy=-100)
    bounce_top(ball, ARENA)
    assert (ball.y, ball.vy) == (200, -100)


def test_no_double_bounce_when_already_moving_down():
    ball = Ball(100, 25, 10, vy=100)
    bounce_top(ball, ARENA)
    assert ball.vy == 100


def test_ball_never_leaks_through_top_at_high_speed():
    ball = Ball(100, -500, 10, vy=-5000)
    bounce_top(ball, ARENA)
    assert ball.y - ball.radius >= ARENA.top
    assert ball.vy > 0
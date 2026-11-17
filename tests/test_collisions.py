from config.settings import RESTITUTION
from entities.arena import Arena
from entities.ball import Ball
from physics.collisions import bounce_left, bounce_right, bounce_top

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


def test_bounce_left_reverses_horizontal_speed():
    ball = Ball(25, 200, 10, vx=-100, vy=30)  # bord gauche à 15, dans le mur
    bounce_left(ball, ARENA)
    assert ball.vx == 100
    assert ball.vy == 30


def test_bounce_left_puts_ball_back_inside():
    ball = Ball(25, 200, 10, vx=-100)
    bounce_left(ball, ARENA)
    assert ball.x == 30  # arena.left + radius


def test_no_bounce_left_when_not_touching():
    ball = Ball(200, 200, 10, vx=-100)
    bounce_left(ball, ARENA)
    assert (ball.x, ball.vx) == (200, -100)


def test_no_double_bounce_left_when_already_moving_right():
    ball = Ball(25, 200, 10, vx=100)
    bounce_left(ball, ARENA)
    assert ball.vx == 100


def test_ball_never_leaks_through_left_at_high_speed():
    ball = Ball(-500, 200, 10, vx=-5000)
    bounce_left(ball, ARENA)
    assert ball.x - ball.radius >= ARENA.left
    assert ball.vx > 0


def test_bounce_right_reverses_horizontal_speed():
    ball = Ball(475, 200, 10, vx=100, vy=30)  # bord droit à 485, dans le mur
    bounce_right(ball, ARENA)
    assert ball.vx == -100
    assert ball.vy == 30


def test_bounce_right_puts_ball_back_inside():
    ball = Ball(475, 200, 10, vx=100)
    bounce_right(ball, ARENA)
    assert ball.x == 470  # arena.right - radius


def test_no_bounce_right_when_not_touching():
    ball = Ball(200, 200, 10, vx=100)
    bounce_right(ball, ARENA)
    assert (ball.x, ball.vx) == (200, 100)


def test_no_double_bounce_right_when_already_moving_left():
    ball = Ball(475, 200, 10, vx=-100)
    bounce_right(ball, ARENA)
    assert ball.vx == -100


def test_ball_never_leaks_through_right_at_high_speed():
    ball = Ball(1000, 200, 10, vx=5000)
    bounce_right(ball, ARENA)
    assert ball.x + ball.radius <= ARENA.right
    assert ball.vx < 0


def test_restitution_is_perfect():
    assert RESTITUTION == 1.0


def test_perfect_bounces_keep_speed_over_many_bounces():
    ball = Ball(100, 200, 10, vx=300, vy=40)
    for _ in range(5000):
        ball.move(1 / 60)
        bounce_left(ball, ARENA)
        bounce_right(ball, ARENA)
        assert ball.x - ball.radius >= ARENA.left
        assert ball.x + ball.radius <= ARENA.right
    assert abs(ball.vx) == 300
    assert ball.vy == 40
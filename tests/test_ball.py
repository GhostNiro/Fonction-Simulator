import pytest
from config.settings import GRAVITY
from entities.ball import Ball


def test_gravity_increases_vertical_speed():
    ball = Ball(0, 0, 10)
    ball.apply_gravity(1.0)
    assert ball.vy == GRAVITY


def test_gravity_does_not_touch_horizontal_speed():
    ball = Ball(0, 0, 10, vx=5)
    ball.apply_gravity(1.0)
    assert ball.vx == 5


def test_gravity_is_framerate_independent():
    one_step = Ball(0, 0, 10)
    one_step.apply_gravity(1 / 30)

    two_steps = Ball(0, 0, 10)
    two_steps.apply_gravity(1 / 60)
    two_steps.apply_gravity(1 / 60)

    assert one_step.vy == pytest.approx(two_steps.vy)


def test_move_updates_position_from_velocity():
    ball = Ball(10, 20, 5, vx=100, vy=-50)
    ball.move(0.5)
    assert ball.x == 60
    assert ball.y == -5


def test_move_does_not_change_velocity():
    ball = Ball(0, 0, 5, vx=100, vy=50)
    ball.move(1.0)
    assert (ball.vx, ball.vy) == (100, 50)


def test_move_is_framerate_independent():
    one_step = Ball(0, 0, 5, vx=120, vy=60)
    one_step.move(1 / 30)

    two_steps = Ball(0, 0, 5, vx=120, vy=60)
    two_steps.move(1 / 60)
    two_steps.move(1 / 60)

    assert one_step.x == pytest.approx(two_steps.x)
    assert one_step.y == pytest.approx(two_steps.y)
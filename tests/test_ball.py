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
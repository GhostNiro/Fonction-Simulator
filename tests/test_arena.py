from config.settings import (
    ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
)
from entities.arena import Arena


def test_walls_positions():
    arena = Arena(20, 20, 460, 660)
    assert arena.left == 20
    assert arena.right == 480
    assert arena.top == 20
    assert arena.bottom == 680


def test_arena_fits_in_window():
    arena = Arena(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
    assert arena.left >= 0 and arena.top >= 0
    assert arena.right <= WINDOW_WIDTH
    assert arena.bottom <= WINDOW_HEIGHT
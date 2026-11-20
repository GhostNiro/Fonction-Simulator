import pygame
from config.settings import (
    ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT, WALL_THICKNESS,
    WINDOW_WIDTH, WINDOW_HEIGHT, MAX_WALL_POINTS,
)
from entities.arena import Arena
from entities.score_wall import ScoreWall
from ui.wall_points_display import WallPointsDisplay, format_points

pygame.font.init()

ARENA = Arena(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
WALL_RECT = pygame.Rect(ARENA.x, ARENA.bottom, ARENA.width, WALL_THICKNESS)


def pixels(surface, rect):
    return pygame.image.tostring(surface.subsurface(rect), "RGB")


def test_format_points_is_readable():
    assert format_points(100) == "100"
    assert format_points(1000) == "1 000"
    assert format_points(10**12) == "1 000 000 000 000"


def test_wall_band_fits_in_window():
    assert WALL_RECT.bottom <= WINDOW_HEIGHT


def test_max_points_fit_in_wall_band():
    width, height = WallPointsDisplay().font.size(format_points(MAX_WALL_POINTS))
    assert width <= ARENA_WIDTH
    assert height <= WALL_THICKNESS


def test_points_are_drawn_on_the_wall_only():
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    WallPointsDisplay().draw(surface, ScoreWall(100), ARENA)
    arena_rect = pygame.Rect(ARENA.x, ARENA.top, ARENA.width, ARENA_HEIGHT)
    assert pixels(surface, WALL_RECT) != bytes(WALL_RECT.w * WALL_RECT.h * 3)
    assert pixels(surface, arena_rect) == bytes(arena_rect.w * arena_rect.h * 3)


def test_display_updates_after_a_hit():
    display = WallPointsDisplay()
    wall = ScoreWall(100)

    before = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.draw(before, wall, ARENA)

    wall.hit()
    after = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.draw(after, wall, ARENA)

    assert pixels(before, WALL_RECT) != pixels(after, WALL_RECT)
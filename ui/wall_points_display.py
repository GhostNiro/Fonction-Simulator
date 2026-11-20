import pygame
from config.settings import TEXT_COLOR, WALL_THICKNESS


def format_points(points):
    """1000000 -> '1 000 000' (plus lisible)."""
    return f"{points:,}".replace(",", " ")


class WallPointsDisplay:
    """Affiche les points restants, centrés sur la bande du mur du bas."""

    def __init__(self):
        self.font = pygame.font.Font(None, 28)  # créée une seule fois

    def draw(self, surface, wall, arena):
        wall_rect = pygame.Rect(arena.x, arena.bottom, arena.width, WALL_THICKNESS)
        text = self.font.render(format_points(wall.points), True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=wall_rect.center))
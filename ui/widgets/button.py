import pygame
from config.settings import BUTTON_ON_COLOR, BUTTON_OFF_COLOR, TEXT_COLOR
class Button :
    def __init__(self, x, y, width, height, text, enabled=False, on_click = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click
        self.enabled = enabled
        self.font = pygame.font.Font(None, 36)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        """À appeler dans la boucle principale pour chaque événement pygame."""
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.get_rect().collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
 

    def draw(self, surface):
        color = BUTTON_ON_COLOR if self.enabled else BUTTON_OFF_COLOR
        pygame.draw.rect(surface, color, self.get_rect())
 
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        surface.blit(
            text_surface,
            (self.x + self.width // 2 - text_surface.get_width() // 2,
             self.y + self.height // 2 - text_surface.get_height() // 2)
        )
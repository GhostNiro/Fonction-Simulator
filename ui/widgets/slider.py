import pygame
from config.settings import SLIDER_BAR_COLOR, SLIDER_HANDLE_COLOR, TEXT_COLOR
 
 
class Slider:
    def __init__(self, x, y, width, height, label, min_value, max_value, default_value=None, step=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = default_value if default_value is not None else min_value
 
        self.handle_width = 20
        self.handle_height = 30
        self.dragging = False
        self.font = pygame.font.Font(None, 26)  # créée une seule fois
 
    def _value_to_x(self):
        """Calcule la position x de la poignée en fonction de la valeur actuelle."""
        usable_width = self.width - self.handle_width
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        return self.x + int(ratio * usable_width)
 
    def _x_to_value(self, pos_x):
        """Calcule la valeur correspondant à une position x de souris."""
        usable_width = self.width - self.handle_width
        ratio = (pos_x - self.x) / usable_width
        ratio = max(0.0, min(1.0, ratio))  # on borne entre 0 et 1
        raw_value = self.min_value + ratio * (self.max_value - self.min_value)
        stepped_value = round(raw_value / self.step) * self.step
        return max(self.min_value, min(self.max_value, stepped_value))
 
    def _handle_rect(self):
        handle_x = self._value_to_x()
        return pygame.Rect(
            handle_x,
            self.y + self.height // 2 - self.handle_height // 2,
            self.handle_width,
            self.handle_height,
        )
 
    def handle_event(self, event):
        """À appeler dans la boucle principale pour chaque événement pygame."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.value = self._x_to_value(event.pos[0])
 
    def get_value(self):
        return self.value
 
    def draw(self, surface):
        # Barre du slider
        pygame.draw.rect(
            surface, SLIDER_BAR_COLOR,
            (self.x, self.y + self.height // 2 - 5, self.width, 10)
        )
 
        # Poignée positionnée selon la valeur réelle
        handle_rect = self._handle_rect()
        pygame.draw.rect(surface, SLIDER_HANDLE_COLOR, handle_rect)
 
        # Label + valeur courante affichée
        label_text = self.font.render(f"{self.label} : {self.value}", True, TEXT_COLOR)
        surface.blit(
            label_text,
            (self.x + self.width // 2 - label_text.get_width() // 2,
             self.y - label_text.get_height() - 5)
        )
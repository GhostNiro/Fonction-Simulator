import pygame
from config.settings import (
    TEXT_COLOR,
    INPUT_BG_COLOR,
    INPUT_BORDER_COLOR,
    INPUT_BORDER_ACTIVE_COLOR,
    PLACEHOLDER_COLOR,
    HINT_COLOR,
)
 
 
class TextInput:
    """
    Champ de texte basique : cliquable, capture la saisie clavier.
    Ne valide RIEN pour l'instant (pas de parseur branché) — ça viendra
    dans une US dédiée (Epic 5 / US 5.4, US 5.5).
    """
 
    def __init__(self, x, y, width, height, label="", placeholder="", hint=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.placeholder = placeholder
        self.hint = hint  # peut contenir des retours à la ligne "\n"
        self.text = ""
        self.active = False
 
        self.label_font = pygame.font.Font(None, 26)
        self.text_font = pygame.font.Font(None, 28)
        self.hint_font = pygame.font.Font(None, 18)
 
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Actif si on clique dedans, inactif si on clique ailleurs
            self.active = self.get_rect().collidepoint(event.pos)
 
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False  # on considère la saisie "validée" (pour l'instant, juste désactivée)
 
        elif event.type == pygame.TEXTINPUT and self.active:
            # Événement pygame dédié à la saisie de texte (gère les caractères correctement)
            self.text += event.text
 
    def get_value(self):
        return self.text
 
    def draw(self, surface):
        # Label au-dessus du champ (ex. "Formule (en x)")
        if self.label:
            label_surface = self.label_font.render(self.label, True, TEXT_COLOR)
            surface.blit(label_surface, (self.x, self.y - label_surface.get_height() - 5))
 
        # Le champ lui-même
        border_color = INPUT_BORDER_ACTIVE_COLOR if self.active else INPUT_BORDER_COLOR
        pygame.draw.rect(surface, INPUT_BG_COLOR, self.get_rect())
        pygame.draw.rect(surface, border_color, self.get_rect(), width=2)
 
        # Texte tapé, ou placeholder si vide
        if self.text:
            display_text, color = self.text, TEXT_COLOR
        else:
            display_text, color = self.placeholder, PLACEHOLDER_COLOR
 
        text_surface = self.text_font.render(display_text, True, color)
        surface.blit(
            text_surface,
            (self.x + 8, self.y + self.height // 2 - text_surface.get_height() // 2)
        )
 
        # Texte d'aide sous le champ (règles de syntaxe), potentiellement multi-lignes
        if self.hint:
            for i, line in enumerate(self.hint.split("\n")):
                hint_surface = self.hint_font.render(line, True, HINT_COLOR)
                surface.blit(
                    hint_surface,
                    (self.x, self.y + self.height + 6 + i * (hint_surface.get_height() + 2))
                )
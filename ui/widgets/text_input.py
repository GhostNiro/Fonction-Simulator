import pygame
from config.settings import (
    TEXT_COLOR,
    INPUT_BG_COLOR,
    INPUT_BORDER_COLOR,
    INPUT_BORDER_ACTIVE_COLOR,
    INPUT_BORDER_INVALID_COLOR,
    PLACEHOLDER_COLOR,
    HINT_COLOR,
)


class TextInput:
    """
    Champ de texte basique : cliquable, capture la saisie clavier.

    - numbers_only=True : seuls les chiffres sont acceptés à la saisie.
    - required=True (défaut) : un champ vide est considéré comme invalide.
    - max_value : plafond optionnel. Si la saisie dépasse cette valeur,
      elle est automatiquement ramenée à max_value (US 1.7).

    is_valid() et get_error_message() partagent la même source de vérité :
    is_valid() == (get_error_message() is None).
    """

    def __init__(self, x, y, width, height, label="", placeholder="", hint="",
                 numbers_only=False, default_value="", required=True, max_value=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.placeholder = placeholder
        self.hint = hint  # peut contenir des retours à la ligne "\n"
        self.numbers_only = numbers_only
        self.required = required
        self.max_value = max_value
        self.default_value = default_value
        self.text = self.default_value
        self.active = False

        self.label_font = pygame.font.Font(None, 26)
        self.text_font = pygame.font.Font(None, 28)
        self.hint_font = pygame.font.Font(None, 18)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_error_message(self):
        """Retourne None si le champ est valide, sinon un message clair."""
        if self.text == "":
            if self.required:
                return "Ce champ est obligatoire"
            return None

        if self.numbers_only:
            # Grâce au filtre à la saisie, self.text ne contient que des chiffres.
            value = int(self.text)
            if value <= 0:
                return "Doit être un entier strictement positif"
            if self.max_value is not None and value > self.max_value:
                return f"Ne peut pas dépasser {self.max_value}"

        return None

    def is_valid(self):
        return self.get_error_message() is None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.get_rect().collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False

        elif event.type == pygame.TEXTINPUT and self.active:
            if self.numbers_only and not event.text.isdecimal():
                return  # caractère refusé, on ignore silencieusement

            new_text = self.text + event.text

            # Plafond : si la saisie dépasse max_value, on la ramène à max_value.
            if self.numbers_only and self.max_value is not None and new_text != "":
                if int(new_text) > self.max_value:
                    new_text = str(self.max_value)

            self.text = new_text

    def get_value(self):
        return self.text

    def reset(self):
        self.text = self.default_value
        self.active = False

    def draw(self, surface):
        # Label au-dessus du champ
        if self.label:
            label_surface = self.label_font.render(self.label, True, TEXT_COLOR)
            surface.blit(label_surface, (self.x, self.y - label_surface.get_height() - 5))

        # Couleur de bordure : rouge si invalide, sinon vert (actif) ou gris (inactif)
        if not self.is_valid():
            border_color = INPUT_BORDER_INVALID_COLOR
        elif self.active:
            border_color = INPUT_BORDER_ACTIVE_COLOR
        else:
            border_color = INPUT_BORDER_COLOR

        pygame.draw.rect(surface, INPUT_BG_COLOR, self.get_rect())
        pygame.draw.rect(surface, border_color, self.get_rect(), width=2)

        # Texte tapé, ou placeholder si vide
        if self.text:
            display_text, color = self.text, TEXT_COLOR
        else:
            display_text, color = self.placeholder, PLACEHOLDER_COLOR

        text_surface = self.text_font.render(display_text, True, color)

        # Défilement horizontal pour garder la FIN du texte visible
        visible_width = self.width - 16
        text_width = text_surface.get_width()
        offset_x = max(0, text_width - visible_width)

        previous_clip = surface.get_clip()
        surface.set_clip(self.get_rect())
        surface.blit(
            text_surface,
            (self.x + 8 - offset_x, self.y + self.height // 2 - text_surface.get_height() // 2)
        )
        surface.set_clip(previous_clip)

        # Message d'erreur en priorité ; sinon, texte d'aide (multi-lignes)
        error = self.get_error_message()
        if error:
            error_surface = self.hint_font.render(error, True, INPUT_BORDER_INVALID_COLOR)
            surface.blit(error_surface, (self.x, self.y + self.height + 6))
        elif self.hint:
            for i, line in enumerate(self.hint.split("\n")):
                hint_surface = self.hint_font.render(line, True, HINT_COLOR)
                surface.blit(
                    hint_surface,
                    (self.x, self.y + self.height + 6 + i * (hint_surface.get_height() + 2))
                )
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
    Si numbers_only=True, seuls les chiffres sont acceptés à la saisie,
    et is_valid() vérifie qu'il y a bien une valeur strictement positive
    (US 1.5 : pas de champ vide, pas de zéro).
    Pour un champ libre (numbers_only=False, ex. la formule), is_valid()
    retourne toujours True pour l'instant — sa validation viendra dans
    une US dédiée (Epic 5).
    """

    def __init__(self, x, y, width, height, label="", placeholder="", hint="",
                 numbers_only=False, default_value=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.placeholder = placeholder
        self.hint = hint  # peut contenir des retours à la ligne "\n"
        self.numbers_only = numbers_only
        self.text = default_value
        self.active = False

        self.label_font = pygame.font.Font(None, 26)
        self.text_font = pygame.font.Font(None, 28)
        self.hint_font = pygame.font.Font(None, 18)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_valid(self):
        if not self.numbers_only:
            return True
        # Grâce au filtre à la saisie, self.text ne peut contenir que des
        # chiffres (0-9) ou être vide : int() ne peut donc pas planter ici.
        return self.text != "" and int(self.text) > 0

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
            if self.numbers_only and not event.text.isnumeric():
                return  # caractère refusé, on ignore silencieusement
            self.text += event.text

    def get_value(self):
        return self.text

    def draw(self, surface):
        # Label au-dessus du champ (ex. "Formule (en x)")
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

        # Défilement horizontal : si le texte est plus large que la zone
        # visible, on décale vers la gauche pour garder la FIN du texte
        # visible (c'est là que l'utilisateur tape/efface en ce moment).
        visible_width = self.width - 16  # marge de 8px de chaque côté
        text_width = text_surface.get_width()
        offset_x = max(0, text_width - visible_width)

        # On restreint temporairement la zone de dessin au cadre du champ,
        # pour que le texte décalé ne déborde jamais visuellement dessus.
        previous_clip = surface.get_clip()
        surface.set_clip(self.get_rect())
        surface.blit(
            text_surface,
            (self.x + 8 - offset_x, self.y + self.height // 2 - text_surface.get_height() // 2)
        )
        surface.set_clip(previous_clip)

        # Texte d'aide sous le champ, potentiellement multi-lignes
        if self.hint:
            for i, line in enumerate(self.hint.split("\n")):
                hint_surface = self.hint_font.render(line, True, HINT_COLOR)
                surface.blit(
                    hint_surface,
                    (self.x, self.y + self.height + 6 + i * (hint_surface.get_height() + 2))
                )
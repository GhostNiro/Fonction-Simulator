import pygame
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS
from ui.widgets.slider import Slider
from ui.widgets.button import Button
from ui.widgets.text_input import TextInput

# --- Initialisation pygame ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# --- Sliders (nombre / taille / vitesse des balles) ---
ball_count_slider = Slider(
    x=530, y=40, width=220, height=40,
    label="Nombre de balles",
    min_value=1, max_value=20,
    default_value=1,
    step=1,
)

ball_size_slider = Slider(
    x=530, y=120, width=220, height=40,
    label="Taille des balles",
    min_value=5, max_value=50,
    default_value=5,
    step=1,
)

ball_speed_slider = Slider(
    x=530, y=200, width=220, height=40,
    label="Vitesse des balles",
    min_value=1, max_value=10,
    default_value=1,
    step=1,
)

sliders = [ball_count_slider, ball_size_slider, ball_speed_slider]

# Champ "points du mur" (US 1.5) : nombre entier libre, pas de limite haute
# imposée par un slider. numbers_only=True filtre la saisie aux chiffres,
# is_valid() interdit le champ vide ou une valeur de 0.
wall_points_input = TextInput(
    x=530, y=280, width=220, height=40,
    label="Points du mur du bas",
    numbers_only=True,
    default_value="100",
    hint="nombre entier positif (pas de 0)",
)

# Champ de saisie de la formule (US 1.6). Pas de validation ni de menu
# déroulant de suggestions pour l'instant (ça viendra en US 5.4 et US 5.7).
formula_input = TextInput(
    x=530, y=365, width=220, height=40,
    label="Formule (en x)",
    placeholder="ex : x**2",
    hint="+ - * / **  sqrt()  factorial()\nlog()  abs()  root(x, n)",
)

text_inputs = [wall_points_input, formula_input]


def on_start_click():
    # Placeholder pour l'instant : le vrai lancement de la simulation
    # sera implémenté en US 6.1. On vérifie juste ici que le clic fonctionne.
    print("Démarrer cliqué ! Valeurs choisies :")
    for slider in sliders:
        print(f"  - {slider.label} : {slider.get_value()}")
    print(f"  - Points du mur : {wall_points_input.get_value()}")
    print(f"  - Formule : {formula_input.get_value()}")


# Activé dès le départ car rien, pour l'instant, ne peut rendre la config invalide
# (US 1.7 branchera plus tard enabled sur la validité réelle des champs)
start_button = Button(
    x=565, y=480, width=150, height=50,
    text="Démarrer",
    enabled=True,
    on_click=on_start_click,
)

# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for slider in sliders:
            slider.handle_event(event)

        for text_input in text_inputs:
            text_input.handle_event(event)

        start_button.handle_event(event)

    screen.fill((30, 30, 30))  # fond gris foncé

    for slider in sliders:
        slider.draw(screen)

    for text_input in text_inputs:
        text_input.draw(screen)

    start_button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
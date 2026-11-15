from config.settings import GRAVITY


class Ball:
    def __init__(self, x, y, radius, vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy

    def apply_gravity(self, dt):
        """dt = temps écoulé en secondes depuis la dernière frame."""
        self.vy += GRAVITY * dt
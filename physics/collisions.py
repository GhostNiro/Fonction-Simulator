from config.settings import RESTITUTION


def bounce_top(ball, arena):
    """Rebond sur le mur du haut."""
    if ball.y - ball.radius < arena.top and ball.vy < 0:
        ball.y = arena.top + ball.radius
        ball.vy = -ball.vy * RESTITUTION


def bounce_left(ball, arena):
    """Rebond sur le mur de gauche."""
    if ball.x - ball.radius < arena.left and ball.vx < 0:
        ball.x = arena.left + ball.radius
        ball.vx = -ball.vx * RESTITUTION


def bounce_right(ball, arena):
    """Rebond sur le mur de droite."""
    if ball.x + ball.radius > arena.right and ball.vx > 0:
        ball.x = arena.right - ball.radius
        ball.vx = -ball.vx * RESTITUTION


def hits_bottom(ball, arena):
    """True si la balle descend et touche le mur du bas (compté une fois par impact)."""
    return ball.y + ball.radius > arena.bottom and ball.vy > 0
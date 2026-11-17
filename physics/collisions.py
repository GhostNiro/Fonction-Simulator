from config.settings import RESTITUTION


def bounce_top(ball, arena):
    """Rebond sur le mur du haut. La position est réfléchie (et non simplement
    recalée) pour ne pas perdre d'énergie sous l'effet de la gravité."""
    limit = arena.top + ball.radius
    if ball.y < limit and ball.vy < 0:
        ball.y = 2 * limit - ball.y
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


def bounce_bottom(ball, arena):
    """Rebond sur le mur du bas (position réfléchie, comme pour le haut).
    Retourne True s'il y a eu impact, pour que la simulation puisse le compter."""
    if not hits_bottom(ball, arena):
        return False
    limit = arena.bottom - ball.radius
    ball.y = 2 * limit - ball.y
    ball.vy = -ball.vy * RESTITUTION
    return True
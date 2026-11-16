def bounce_top(ball, arena):
    """Rebond parfait sur le mur du haut."""
    if ball.y - ball.radius < arena.top and ball.vy < 0:
        ball.y = arena.top + ball.radius
        ball.vy = -ball.vy
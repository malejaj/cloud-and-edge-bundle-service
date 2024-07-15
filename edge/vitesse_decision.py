def vitesse_decision(dist, vitesse):
    if dist < 20:
        return 0
    elif dist < 40:
        return 1
    return 2
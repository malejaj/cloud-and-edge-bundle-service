def vitesse_decision(dist, vitesse):
    if dist < 80:
        return 0
    elif dist < 100:
        return 1
    return 2
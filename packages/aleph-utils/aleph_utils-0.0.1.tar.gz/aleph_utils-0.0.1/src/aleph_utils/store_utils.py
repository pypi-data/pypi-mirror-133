import numpy as np
from datetime import datetime


def get_fragment():
    return np.random.randint(100000)


def make_fragments():
    """
    Génère des fragments à partir de la date du jour exprimée en millionièmes de seconde.
    Pour l'utiliser, on déclare une variable qui appelle la fonction puis on itère avec next().
    Exemple:
    fragments = make_fragments()
    print(next(fragments)  # 1ère itération
    print(next(fragments)  # 2e itération
    ...
    """
    n = int(datetime.timestamp(datetime.today()) * 10**6)
    while True:
        yield n
        n += 1
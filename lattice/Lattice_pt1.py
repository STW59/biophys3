import random
import numpy as np

CHAIN_LENGTH = 6


def main():
    residue_loc = []
    residue_loc.append([0, 0])  # Residue 0 set to (0, 0)

    loc = random.randint(0, 1)
    if loc == 0:
        residue_loc.append([random.randint(-1, 1), 0])  # Residue 1 is in random location adjacent to the origin
    else:
        residue_loc.append([0, random.randint(-1, 1)])

    for residue in range(1, CHAIN_LENGTH):
        x_last = residue_loc[residue - 1][0]
        y_last = residue_loc[residue - 1][1]
        angle = random.randint(-1, 1)

        x_new = 0
        y_new = 0
        while [x_new, y_new] in residue_loc:
            x_new = int(x_last + 1 * np.cos(angle * (np.pi/2)))
            y_new = int(y_last + 1 * np.sin(angle * (np.pi/2)))
        residue_loc.append([x_new, y_new])

    print(residue_loc)


main()

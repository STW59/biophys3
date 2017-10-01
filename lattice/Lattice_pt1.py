import numpy as np
import random
import time


def generate_lattice(chain_length):
    """
    Generates a lattice model given a starting chain length.
    :param chain_length: integer value for the length of the chain
    :return: list of residue coordinates and elapsed process time as [chain_length, [coordinates], time]
    """
    start_time = time.clock()  # Start performance timer

    residue_loc = []

    # Residue 0 set to (0, 0)
    residue_loc.append([0, 0])

    # Residue 1 is in random location adjacent to the origin
    loc = random.randint(0, 1)
    x_new, y_new = 0, 0
    if loc == 0:
        while [x_new, y_new] in residue_loc:  # Check for self-intersections
            x_new = random.randint(-1, 1)  # Residue 1 is changed in x

    else:
        while [x_new, y_new] in residue_loc:
            y_new = random.randint(-1, 1)  # Residue 1 is changed in y

    residue_loc.append([x_new, y_new])

    # Iterate residues 2 to chain_length
    for residue in range(2, chain_length):
        iteration_count = 0
        x_last = residue_loc[residue - 1][0]
        y_last = residue_loc[residue - 1][1]

        while [x_new, y_new] in residue_loc:  # Check for self-intersections
            if iteration_count > 10000 * chain_length:  # Terminate the calculations if it always self-intersects
                print('Failed to find non-intersecting solution.')
                break

            angle = random.randint(0, 3)
            x_new = x_last + int(np.cos(angle * (np.pi/2)))
            y_new = y_last + int(np.sin(angle * (np.pi/2)))

            iteration_count += 1
        residue_loc.append([x_new, y_new])

    end_time = time.clock()  # End performance timer
    return [chain_length, residue_loc, end_time - start_time]


def main():
    chain = generate_lattice(4)
    print(chain[2])


main()

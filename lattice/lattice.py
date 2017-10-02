import time


def generate_lattice(chain_length):
    """
    Generates a lattice model given a starting chain length.
    :param chain_length: integer value for the length of the chain
    :return: list of residue coordinates and elapsed process time as [chain_length, [coordinates], time]
    """
    start_time = time.clock()  # Start performance timer

    x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
    y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
    next_step = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
    n = chain_length - 2  # Index of last bond
    conformation = ['u' for i in range(n + 1)]
    first_r = n

    while True:
        x = 0  # x coordinate
        y = 0  # y coordinate
        j = 0  # Residue number

        residue_loc = {(x, y): j}  # Residue locations indexed by residue number
        residue_coords = [(x, y)]  # Non-indexed residue locations

        for c in conformation:
            x += x_step[c]
            y += y_step[c]
            coord = (x, y)

            if coord in residue_loc:
                i = n
                conformation[i] = next_step[conformation[i]]
                while conformation[i] is 'u':
                    i -= 1
                break
            j += 1
            residue_loc[coord] = j
            residue_coords.append(coord)
        else:
            i = n
            conformation[i] = next_step[conformation[i]]
            while conformation[i] is 'u':
                i -= 1
                conformation[i] = next_step[conformation[i]]

            print(residue_coords)
            if first_r is 0:
                break

    end_time = time.clock()
    return end_time - start_time


def main():
    chain = generate_lattice(4)
    print(chain)


main()

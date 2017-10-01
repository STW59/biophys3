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
    opposite_pos = {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}
    n = chain_length - 2
    conformation = ['u' for i in range(n + 1)]
    first_r = n
    n_count = 0

    while True:
        x = 0
        y = 0
        j = 0

        residue_loc = {(x, y): j}
        residue_coords = [(x, y)]

        for c in conformation:
            x += x_step[c]
            y += y_step[c]
            coord = (x, y)
            if coord in residue_loc:
                for k in range(j + 1, n + 1):
                    conformation[k] = 'u'
                conformation[j] = next_step[conformation[j]]
                while conformation[j] == 'u':
                    j -= 1
                    conformation[j] = next_step[conformation[j]]
                if j == first_r and conformation[j] not in ['r', 'u']:
                    first_r -= 1
                    conformation[first_r] = 'r'
                    for k in range(j, n + 1):
                        conformation[k] = 'u'
                break
            j += 1
            residue_loc[coord] = j
            residue_coords.append(coord)
        else:
            i = n
            conformation[i] = next_step[conformation[i]]
            while conformation[i] == 'u':
                i -= 1

            if i == first_r and conformation[i] not in ['r', 'u']:
                first_r -= 1
                conformation[first_r] = 'r'
                for j in range(i, n + 1):
                    conformation[j] = 'u'
            print(residue_coords)
        if first_r == 0:
            break

    end_time = time.clock()  # End performance timer
    return end_time - start_time


def main():
    chain = generate_lattice(4)
    print(chain)


main()

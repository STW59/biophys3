"""
File authored by Stephen E. White
STW59@pitt.edu

Algorithm modified from: https://github.com/jbloomlab/latticeproteins
"""
import pickle
import time


class LatticeGen:
    def __init__(self, chain_length):
        self.__chain_length = chain_length

    def chain_length(self):
        return self.__chain_length

    @staticmethod
    def generate_lattice(chain_length):
        """
        Generates a lattice model given a starting chain length.
        :param chain_length: integer value for the length of the chain
        :return: Elapsed process time
        """
        start_time = time.clock()  # Start performance timer

        x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
        y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
        next_step = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
        n = chain_length - 2  # Index of last bond
        conformation = ['u' for i in range(n + 1)]
        first_r = n

        export_file = open('lattice_{}.dat'.format(chain_length), 'wb')

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
                if coord in residue_loc:  # Look for an intersection
                    for k in range(j + 1, n + 1):  # Try again at that step
                        conformation[k] = 'u'
                    conformation[j] = next_step[conformation[j]]
                    while conformation[j] == 'u':
                        j -= 1
                        conformation[j] = next_step[conformation[j]]
                    if j == first_r and conformation[j] not in ['u', 'r']:
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
                    conformation[i] = next_step[conformation[i]]

                if i == first_r and conformation[i] not in ['u', 'r']:
                    first_r -= 1
                    conformation[first_r] = 'r'
                    for j in range(i, n + 1):
                        conformation[j] = 'u'
                pickle.dump(residue_coords, export_file)

                if first_r == 0:
                    break

        end_time = time.clock()  # End performance timer
        export_file.close()
        return end_time - start_time

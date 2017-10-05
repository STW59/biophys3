import pickle
import random


class MonteCarlo:
    def __init__(self):
        pass
    # TODO: code getters and setters for each parameter

    # TODO: look up Markov process

    @staticmethod
    def direction_change(n_coord, n1_coord):
        """
        This method randomly changes the direction of the selected coordinates.
        :param n_coord: (x, y) for selected residue
        :param n1_coord: (x, y) for residue after selected residue
        :return: new bond direction for after randomly selected residue
        """
        bond_directions = ['u', 'r', 'd', 'l']

        # Determine bond direction
        if n_coord[1] < n1_coord[1]:  # up
            new_dir = direction = 'u'
        elif n_coord[0] < n1_coord[0]:  # right
            new_dir = direction = 'r'
        elif n_coord[1] > n1_coord[1]:  # down
            new_dir = direction = 'd'
        elif n_coord[0] > n1_coord[0]:  # left
            new_dir = direction = 'l'
        else:
            print('Error in coordinates.')

        while new_dir is direction:
            new_dir = bond_directions[random.randint(0, 3)]
        return new_dir

    @staticmethod
    def bond_rotate(chain_length):
        f = open('\data\lattice_{}.dat'.format(chain_length), 'rb')
        structure_count = 0

        # TODO: read a random line of the pickle file and save its data to an array
        try:
            structure = pickle.load(f)
            while structure:
                structure_count += 1
                structure = pickle.load(f)
        except EOFError:
            pass
        finally:
            print(structure_count)
            f.close()

        f = open('\data\lattice_{}.dat'.format(chain_length), 'rb')
        try:
            structure = pickle.load(f)
            for i in range(random.randint(0, structure_count)):
                structure = pickle.load(f)
            print(structure)
        except EOFError:
            pass
        finally:
            f.close()

        # TODO: select a random bond in the selected line to change
        # TODO: rotate the bond and calculate new positions, checking for clashes along the way
        # if clash, reject
        # TODO: calculate acceptance rate


def main():
    MonteCarlo.bond_rotate(8)


main()

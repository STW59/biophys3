import numpy as np
import pickle
import random


class MonteCarlo:
    def __init__(self):
        pass

    @staticmethod
    def get_direction(n_coord, n1_coord):
        direction = ''
        if n_coord[1] < n1_coord[1]:  # up
            direction = 'u'
        elif n_coord[0] < n1_coord[0]:  # right
            direction = 'r'
        elif n_coord[1] > n1_coord[1]:  # down
            direction = 'd'
        elif n_coord[0] > n1_coord[0]:  # left
            direction = 'l'
        else:
            print('Error in coordinates.')

        return direction

    @staticmethod
    def direction_change(direction):
        bond_directions = ['u', 'r', 'd', 'l']
        new_direction = direction
        while new_direction is direction:
            new_direction = bond_directions[random.randint(0, 3)]
        rotation = MonteCarlo.get_rotation(direction, new_direction)
        return new_direction, rotation

    @staticmethod
    def get_rotation(old_bond, new_bond):
        if old_bond is 'u':
            if new_bond is 'r':
                return {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
            elif new_bond is 'd':
                return {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}
            elif new_bond is 'l':
                return {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u'}
        elif old_bond is 'r':
            if new_bond is 'u':
                return {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u'}
            elif new_bond is 'd':
                return {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
            elif new_bond is 'l':
                return {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}
        elif old_bond is 'd':
            if new_bond is 'u':
                return {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}
            elif new_bond is 'r':
                return {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u'}
            elif new_bond is 'l':
                return {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
        elif old_bond is 'l':
            if new_bond is 'u':
                return {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
            elif new_bond is 'r':
                return {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}
            elif new_bond is 'd':
                return {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u'}
        else:
            print('Invalid bond')

    @staticmethod
    def pivot(chain_length):
        # Count the number of structures for the chain_length
        f = open('\data\lattice_{}.dat'.format(chain_length), 'rb')
        structure_count = 0
        try:
            structure = pickle.load(f)
            while structure:
                structure_count += 1
                structure = pickle.load(f)
        except EOFError:
            pass
        finally:
            f.close()

        reject_rate_list = []
        # Average reject rate over 20% of structures
        for r in range(0, structure_count // 5):
            # Get a random structure from the data set
            try:
                f = open('\data\lattice_{}.dat'.format(chain_length), 'rb')
                structure = pickle.load(f)
                for i in range(random.randint(0, structure_count)):
                    structure = pickle.load(f)
            except EOFError:
                pass
            finally:
                f.close()

            # Perform chain_length sweeps of the structure
            for sweeps in range(0, chain_length):
                # Read bonds into a list
                results = []
                bonds = []
                for atom in range(len(structure) - 1):
                    bonds.append(MonteCarlo.get_direction(structure[atom], structure[atom + 1]))\

                # Attempt 10 moves on the random bond
                for moves in range(0, 10):
                    # Change the direction of a random bond
                    new_bonds = bonds.copy()
                    bond_change_index = random.randint(0, len(bonds) - 1)
                    direction = MonteCarlo.direction_change(new_bonds[bond_change_index])
                    new_bonds[bond_change_index] = direction[0]

                    # Determine rotation (cw, ccw, flip)
                    rotation = direction[1]

                    # Adjust the remainder of the bonds
                    for bond in range(bond_change_index + 1, len(bonds)):
                        new_bonds[bond] = rotation[bonds[bond]]

                    # Build new structure coordinates
                    bond = ''
                    x = 0
                    y = 0
                    x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
                    y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
                    new_structure = [(x, y)]
                    for bond in new_bonds:
                        x += x_step[bond]
                        y += y_step[bond]
                        coord = (x, y)
                        if coord not in new_structure:
                            new_structure.append(coord)
                        else:
                            # print('Reject structure')
                            results.append('Reject')
                            break
                        results.append('Accept')

            # Calculate acceptance rate
            reject_rate = results.count('Reject') / len(results)
            reject_rate_list.append(reject_rate)
        reject_rate_list = np.array(reject_rate_list)
        print('Average reject rate = {:.3f}'.format(np.average(reject_rate_list)))


def main():
    chain_length = 8
    for i in range(1):
        MonteCarlo.pivot(chain_length)


main()

import gomodel as go
import montecarlo as mc
import numpy as np
import os
import pickle
import random
import randomstructure as rs
import time

OLD_STRUCTURE_DATA = 'data/old_structure_data.dat'
TRIAL_STRUCTURE_DATA = 'data/trial_structure_data.dat'
NEW_STRUCTURE_DATA = 'data/new_structure_data.dat'


class SimAnneal:
    def __init__(self):
        pass

    @staticmethod
    def copy_temp():
        # Create empty old data temp file
        old_structure_data = open(OLD_STRUCTURE_DATA, 'wb')
        old_structure_data.close()

        # Copy new data to old data temp file
        new_structure_data = open(NEW_STRUCTURE_DATA, 'rb')
        old_structure_data = open(OLD_STRUCTURE_DATA, 'wb')

        try:
            data = pickle.load(new_structure_data)
            while data:
                pickle.dump(data, old_structure_data)
                data = pickle.load(new_structure_data)
        except EOFError:
            pass
        finally:
            new_structure_data.close()
            old_structure_data.close()

        # Create empty new data temp file
        new_structure_data = open(NEW_STRUCTURE_DATA, 'wb')
        new_structure_data.close()

        # Create empty trial data temp file
        trial_structure_data = open(TRIAL_STRUCTURE_DATA, 'wb')
        trial_structure_data.close()

    @staticmethod
    def sweep(structure):
        trial_structure_data = open(TRIAL_STRUCTURE_DATA, 'ab')
        # For each structure, perform 100 sweeps
        for sweeps in range(0, 3):
            # Perform moves at 10 random bonds per structure
            for bond_changes in range(0, 1):
                # Read bonds into a list
                bonds = []
                chain_length = len(structure[0])
                for atom in range(len(structure[0]) - 1):
                    bonds.append(mc.MonteCarlo.get_direction(structure[0][atom], structure[0][atom + 1]))

                # Attempt chain_length moves per random bond
                for moves in range(0, chain_length):
                    # Change the direction of a random bond
                    new_bonds = bonds.copy()
                    bond_change_index = random.randint(0, len(bonds) - 1)
                    direction = mc.MonteCarlo.direction_change(new_bonds[bond_change_index],
                                                               new_bonds[bond_change_index - 1])
                    new_bonds[bond_change_index] = direction[0]

                    # Determine rotation (cw, ccw, flip)
                    rotation = direction[1]

                    # Adjust the remainder of the bonds
                    for bond_index in range(bond_change_index + 1, len(bonds)):
                        new_bonds[bond_index] = rotation[bonds[bond_index]]

                    # Build new structure coordinates
                    x = 0
                    y = 0
                    j = 0
                    x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
                    y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
                    new_structure = [(x, y)]
                    residue_locations = {(x, y): j}
                    for bond in new_bonds:
                        x += x_step[bond]
                        y += y_step[bond]
                        j += 1
                        coord = (x, y)
                        if coord not in new_structure:
                            new_structure.append(coord)
                            residue_locations[(x, y)] = j
                        else:
                            attempt = ('Reject', 0)
                    attempt = ('Accept', new_structure, residue_locations)

                    if attempt[0] is 'Accept':
                        attempt_data = attempt[1], attempt[2]  # format: (x, y) list, {(x, y): j} dictionary
                        pickle.dump((structure, attempt_data), trial_structure_data)  # Output the successful structure to a temp file
        trial_structure_data.close()

    @staticmethod
    def anneal(chain_length):
        if not os.path.exists('data/'):
            os.mkdir('data/')

        r = random.uniform(0, 1)

        beta_start = [1., 5., 9.]
        delta = 0.1

        output = open('STW59_Simulated_Annealing_Output.csv', 'w')

        # Generate a random structure of chain_length
        structure_data = rs.RandomStructure.gen_random_structure(chain_length)
        print(structure_data[0])

        output.write('Structure: [{}]\n'.format(structure_data[0]))
        output.write('\n')

        for beta_start_value in beta_start:

            output.write('starting_beta = {}\n'.format(beta_start_value))
            output.write('beta,average_energy\n')
            beta = beta_start_value
            while beta <= 10.0:
                if beta == beta_start_value:
                    # Sweep old structure
                    old_structure = structure_data
                    SimAnneal.sweep(old_structure)
                else:
                    # Move last iteration's new data to old data file
                    SimAnneal.copy_temp()

                    # Sweep all new structures in old data file
                    old_structure_data = open(OLD_STRUCTURE_DATA, 'rb')
                    try:
                        structure = pickle.load(old_structure_data)
                        while structure:
                            old_structure = structure[0]
                            SimAnneal.sweep(old_structure)
                            structure = pickle.load(old_structure_data)
                    except EOFError:
                        pass
                    finally:
                        old_structure_data.close()

                trial_structure_data = open(TRIAL_STRUCTURE_DATA, 'rb')
                new_structure_data = open(NEW_STRUCTURE_DATA, 'wb')
                results = []
                try:
                    trial_data = pickle.load(trial_structure_data)
                    while trial_data:
                        old_structure = trial_data[0]
                        trial_structure = trial_data[1]

                        e_old = go.GoModel.calc_energy(old_structure)
                        e_trial = go.GoModel.calc_energy(trial_structure)

                        if beta * (e_old - e_trial) > np.log(r):  # Accept move
                            results.append(e_trial)
                            pickle.dump(trial_data, new_structure_data)
                        else:  # Reject move
                            results.append(e_old)
                            pickle.dump((old_structure, old_structure), new_structure_data)

                        trial_data = pickle.load(trial_structure_data)
                except EOFError:
                    pass
                finally:
                    new_structure_data.close()

                results_array = np.array(results)
                average_e = np.average(results_array)
                output.write('{},{}\n'.format(beta, average_e))
                print('beta = {} completed'.format(beta))
                print('average energy = {} epsilon'.format(average_e))
                print()
                beta = (1 + delta) * beta
            output.write('\n')


def main():
    start_time = time.clock()
    SimAnneal.anneal(8)
    end_time = time.clock()
    print('time = {}'.format(end_time - start_time))


# main()

"""
Questions for Yan: 
1: Am I supposed to be generating thousands of structures to move forward? Or should I only be moving the lowest
energy structure on to the next round? 

2: Can we hardware accelerate these computations? (Mine will take forever and a day to run...)
"""

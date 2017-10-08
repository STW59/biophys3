import gomodel as go
import montecarlo as mc
import numpy as np
import pickle
import random
import time


class SimAnneal:
    def __init__(self):
        pass

    @staticmethod
    def sweep(structure, chain_length):
        # Read bonds into a list
        bonds = []
        for atom in range(len(structure) - 1):
            bonds.append(mc.MonteCarlo.get_direction(structure[atom], structure[atom + 1]))

        # Attempt chain_length moves on the random bond
        for moves in range(0, chain_length):
            # Change the direction of a random bond
            new_bonds = bonds.copy()
            bond_change_index = random.randint(0, len(bonds) - 1)
            direction = mc.MonteCarlo.direction_change(new_bonds[bond_change_index])
            new_bonds[bond_change_index] = direction[0]

            # Determine rotation (cw, ccw, flip)
            rotation = direction[1]

            # Adjust the remainder of the bonds
            for bond_index in range(bond_change_index + 1, len(bonds)):
                new_bonds[bond_index] = rotation[bonds[bond_index]]

            # Build new structure coordinates
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
                    return 'Reject', 0
            return 'Accept', new_structure

    @staticmethod
    def structure_data_format(structure):
        structure_dict = {}
        for j in range(len(structure)):
            structure_dict[(structure[j][0], structure[j][1])] = j
        return structure, structure_dict

    @staticmethod
    def anneal(chain_length):
        r = random.uniform(0, 1)

        beta_start = [1., 5., 9.]
        delta = 0.1

        output = open('STW59_Simulated_Annealing_Output.csv', 'w')

        # Pick a random structure from data set
        structure = []
        structure_count = mc.MonteCarlo.structure_count(chain_length)
        f = open('data/lattice_{}.dat'.format(chain_length), 'rb')
        try:
            structure = pickle.load(f)
            for i in range(random.randint(1, structure_count)):
                structure = pickle.load(f)
        except EOFError:
            pass
        finally:
            f.close()

        structure_data = SimAnneal.structure_data_format(structure)

        output.write('Structure: [{}]\n'.format(structure))
        output.write('\n')

        for beta_start_value in beta_start:
            output.write('starting_beta = {}\n'.format(beta_start_value))
            output.write('beta,average_energy\n')
            beta = beta_start_value
            while beta <= 10.0:
                results = []
                old_structure = structure_data
                e_old = go.GoModel.calc_energy(old_structure)
                trial_structures = []
                for sweeps in range(0, 101):
                    trial_structures.append(SimAnneal.sweep(structure, chain_length))

                for trial in trial_structures:
                    if trial[0] is 'Accept':
                        e_trial = go.GoModel.calc_energy(SimAnneal.structure_data_format(trial[1]))
                        if beta * (e_old - e_trial) > np.log(r):
                            results.append(e_trial)
                        else:
                            results.append(e_old)
                results_array = np.array(results)
                average_e = np.average(results_array)

                output.write('{},{}\n'.format(beta, average_e))
                beta = (1 + delta) * beta
            output.write('\n')


def main():
    start_time = time.clock()
    SimAnneal.anneal(16)
    end_time = time.clock()
    print('time = {}'.format(end_time - start_time))


# main()

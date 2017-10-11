import gomodel as go
import montecarlo as mc
import numpy as np
import random
import time

OLD_STRUCTURE_DATA = 'data/old_structure_data.dat'
TRIAL_STRUCTURE_DATA = 'data/trial_structure_data.dat'
NEW_STRUCTURE_DATA = 'data/new_structure_data.dat'


class SimAnneal:
    def __init__(self):
        pass

    @staticmethod
    def sweep(bonds, old_structure_data):
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
                return old_structure_data[0], old_structure_data[1]
        return new_structure, residue_locations

    @staticmethod
    def anneal(structure_data, output_file):
        r = random.uniform(0, 1)
        print('RNG value = {}'.format(r))

        beta_start = [1., 5., 9.]
        delta = 0.1

        # Overwrite old or create new output file
        output = open(output_file, 'w')
        output.close()

        # Since there are multiple structures, append results to the output file
        output = open(output_file, 'a')

        # Write structure used to output file
        output.write('Structure: [{}]\n'.format(structure_data[0]))
        output.write('\n')

        for beta_start_value in beta_start:
            # Write starting beta value and headers to output file
            output.write('starting_beta = {}\n'.format(beta_start_value))
            output.write('beta,average_energy\n')

            beta = beta_start_value
            while beta <= 10.0:
                energy_results = []

                if beta == beta_start_value:
                    old_structure = structure_data

                # For each structure, perform 100 sweeps
                for sweeps in range(0, 100):
                    # Perform moves at 10 random bonds per structure
                    for bond_changes in range(0, 1):
                        # Read bonds into a list
                        bonds = []
                        chain_length = len(structure_data[0])
                        for atom in range(len(structure_data[0]) - 1):
                            bonds.append(
                                mc.MonteCarlo.get_direction(structure_data[0][atom], structure_data[0][atom + 1]))

                        # Attempt chain_length moves per random bond
                        for moves in range(0, chain_length):
                            # Change the direction of a random bond
                            trial_structure_data = SimAnneal.sweep(bonds, structure_data)

                            e_old = go.GoModel.calc_energy(old_structure)
                            e_trial = go.GoModel.calc_energy(trial_structure_data)

                            if beta * (e_old - e_trial) > np.log(r):  # Accept move
                                energy_results.append(e_trial)
                                structure_data = trial_structure_data
                            else:  # Reject move
                                energy_results.append(e_old)
                                structure_data = old_structure

                energy_results_array = np.array(energy_results)
                average_e = np.average(energy_results_array)
                output.write('{},{}\n'.format(beta, average_e))

                beta = (1 + delta) * beta
            output.write('\n')


def main():
    start_time = time.clock()
    # structure_data = go.GoModel.generate_structure(0)  # Given compact structure
    structure_data = go.GoModel.generate_structure(1)  # Different compact structure
    SimAnneal.anneal(structure_data)
    end_time = time.clock()
    print('time = {}'.format(end_time - start_time))


# main()

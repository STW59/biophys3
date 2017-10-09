import gomodel as go
import montecarlo as mc
import numpy as np
import pickle
import random
import randomstructure as rs
import time

TEMP_DATA_OLD = 'temp_data_old.dat'
TEMP_DATA_TRIAL = 'temp_data_trial.dat'
TEMP_DATA_NEW = 'temp_data_new.dat'


class SimAnneal:
    def __init__(self):
        pass

    @staticmethod
    def copy_temp():
        # Create empty old data temp file
        temp_data_old = open(TEMP_DATA_OLD, 'wb')
        temp_data_old.close()

        # Copy new data to old data temp file
        temp_data_new = open(TEMP_DATA_NEW, 'rb')
        temp_data_old = open(TEMP_DATA_OLD, 'wb')

        try:
            data = pickle.load(temp_data_new)
            while data:
                pickle.dump(data, temp_data_old)
                data = pickle.load(temp_data_new)
        except EOFError:
            pass
        finally:
            temp_data_new.close()
            temp_data_old.close()

        # Create empty new data temp file
        temp_data_new = open(TEMP_DATA_NEW, 'wb')
        temp_data_new.close()

        # Create empty trial data temp file
        temp_data_trial = open(TEMP_DATA_TRIAL, 'wb')
        temp_data_trial.close()

    @staticmethod
    def sweep(structure):
        temp_data_trial = open(TEMP_DATA_TRIAL, 'ab')
        for sweeps in range(0, 101):
            attempt = mc.MonteCarlo.pivot_sweep(structure[0])
            if attempt[0] is 'Accept':
                attempt_data = attempt[1], attempt[2]  # format: (x, y) list, {(x, y): j} dictionary
                pickle.dump((structure, attempt_data), temp_data_trial)  # Output the successful structure to a temp file
        temp_data_trial.close()

    @staticmethod
    def anneal(chain_length):
        r = random.uniform(0, 1)

        beta_start = [1., 5., 9.]
        delta = 0.1

        output = open('STW59_Simulated_Annealing_Output.csv', 'w')

        # Generate a random structure of chain_length
        structure_data = rs.RandomStructure.gen_random_structure(chain_length)

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
                    temp_data_old = open(TEMP_DATA_OLD, 'rb')
                    try:
                        structure = pickle.load(temp_data_old)
                        while structure:
                            old_structure = structure[0]
                            SimAnneal.sweep(old_structure)
                            structure = pickle.load(temp_data_old)
                    except EOFError:
                        pass
                    finally:
                        temp_data_old.close()

                temp_data_trial = open(TEMP_DATA_TRIAL, 'rb')
                temp_data_new = open(TEMP_DATA_NEW, 'wb')
                try:
                    trial_data = pickle.load(temp_data_trial)
                    while trial_data:
                        results = []
                        old_structure = trial_data[0]
                        trial_structure = trial_data[1]

                        e_old = go.GoModel.calc_energy(old_structure)
                        e_trial = go.GoModel.calc_energy(trial_structure)

                        if beta * (e_old - e_trial) > np.log(r):  # Accept move
                            results.append(e_trial)
                            pickle.dump(trial_data, temp_data_new)
                        else:  # Reject move
                            results.append(e_old)
                            pickle.dump((old_structure, old_structure), temp_data_new)

                        trial_data = pickle.load(temp_data_trial)
                except EOFError:
                    pass
                finally:
                    temp_data_new.close()

                results_array = np.array(results)
                average_e = np.average(results_array)
                output.write('{},{}\n'.format(beta, average_e))
                print('beta = {} completed'.format(beta))
                beta = (1 + delta) * beta
            output.write('\n')


def main():
    start_time = time.clock()
    SimAnneal.anneal(8)
    end_time = time.clock()
    print('time = {}'.format(end_time - start_time))


# main()

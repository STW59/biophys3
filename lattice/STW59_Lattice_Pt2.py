import gomodel as go
import montecarlo as mc
import simanneal as sim
import time


def monte_carlo():
    mc_out = open('STW59_Monte_Carlo_Output.csv', 'w')
    mc_out.write('length,acceptance_rate,run_time\n')

    for length in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        start_time = time.clock()
        average_accept_rate = mc.MonteCarlo.acceptance_rate(length)
        end_time = time.clock()
        mc_out.write('{},{},{}\n'.format(length, average_accept_rate, end_time - start_time))
    mc_out.close()


def go_model():
    return go.main()


def simulated_annealing():
    # Use provided structure
    structure_data = go.GoModel.generate_structure(0)
    output_file = 'STW59_Simulated_Annealing_Given_Output.csv'
    sim.SimAnneal.anneal(structure_data, output_file)

    # Use a different compact structure
    structure_data = go.GoModel.generate_structure(1)
    output_file = 'STW59_Simulated_Annealing_Different_Output.csv'
    sim.SimAnneal.anneal(structure_data, output_file)


def main():
    print('Beginning Monte Carlo block')
    start_time_1 = time.clock()
    monte_carlo()
    end_time = time.clock()
    print('Monte Carlo run time = {:.3f} seconds'.format(end_time - start_time_1))
    print()

    print('Beginning Go Model block')
    start_time = time.clock()
    go_model()
    end_time = time.clock()
    print('Go Model run time = {:.6f} seconds'.format(end_time - start_time))
    print()

    print('Beginning Simulated Annealing block')
    start_time = time.clock()
    simulated_annealing()
    end_time = time.clock()
    print('Simulated annealing run time = {:.3f} seconds'.format(end_time - start_time))
    print()

    print('Overall run time = {:.3f} seconds'.format(end_time - start_time_1))


main()

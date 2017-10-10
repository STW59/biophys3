import gomodel as go
import montecarlo as mc
import simanneal as sim
import time

CHAIN_LENGTH = 20


def pivot_move(length):
    return mc.MonteCarlo.acceptance_rate(length)


def go_model():
    return go.main()


def simulated_annealing(length):
    return sim.SimAnneal.anneal(length)


def main():
    start_time = time.clock()
    pt2_out = open('STW59_Lattice_Output_Pt2.csv', 'w')
    pt2_out.write('length,acceptance_rate,run_time\n')

    for length in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        start_time = time.clock()
        average_accept_rate = pivot_move(length)
        end_time = time.clock()
        pt2_out.write('{},{},{}\n'.format(length, average_accept_rate, end_time - start_time))
    pt2_out.close()
    go_model()
    simulated_annealing(4)
    end_time = time.clock()
    print('Total run time = {:.3f} seconds'.format(end_time - start_time))


main()

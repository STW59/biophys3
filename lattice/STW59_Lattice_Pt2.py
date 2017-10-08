import gomodel as go
import latticegen as lat
import montecarlo as mc
import simanneal as sim
import time

CHAIN_LENGTH = 16


def generate_lattice(length):
    return lat.LatticeGen.generate_lattice(length)


def pivot_move(length):
    return mc.MonteCarlo.acceptance_rate(length)


def go_model():
    return go.main()


def simulated_annealing(length):
    return sim.SimAnneal.anneal(length)


def main():
    start_time = time.clock()
    pt2_out = open('STW59_Lattice_Output_Pt2.csv', 'w')
    pt2_out.write('length,acceptance_rate\n')

    lat.LatticeGen.initialize_lattice()

    for length in range(3, CHAIN_LENGTH + 1):
        generate_lattice(length)
        average_accept_rate = pivot_move(length)
        pt2_out.write('{},{}\n'.format(length, average_accept_rate))
    pt2_out.close()
    go_model()
    simulated_annealing(16)
    end_time = time.clock()
    print('Total run time = {:.3f} seconds'.format(end_time - start_time))


main()

import gyration as gyr
import latticegen as lat
import montecarlo as mc
import pickle
import time

CHAIN_LENGTH = 8


def generate_lattice(length):
    return lat.LatticeGen.generate_lattice(length)


def calc_gyration(length):
    return gyr.Gyration.radius_calc(length)


def pivot_move(length):
    return mc.MonteCarlo.acceptance_rate(length)


def read_data_file(length):
    f = open('lattice_{}.dat'.format(length), 'rb')
    try:
        lattice = pickle.load(f)
        while lattice:
            print(lattice)
            lattice = pickle.load(f)
    except EOFError:
        print()
        print('End of file.')
    finally:
        f.close()


def main():
    start_time = time.clock()
    pt1_out = open('STW59_Lattice_Output_Pt1.csv', 'w')
    pt2_out = open('STW59_Lattice_Output_Pt2.csv', 'w')
    pt1_out.write('length,conformations,time,min_radius,avg_radius\n')
    pt2_out.write('length,acceptance_ratio\n')

    lat.LatticeGen.initialize_lattice()

    for length in range(3, CHAIN_LENGTH + 1):
        lattice = generate_lattice(length)
        # read_data_file(length)
        gyration = calc_gyration(length)
        average_reject_rate = pivot_move(length)

        # pt1_out.write('{},{},{}\n'.format(length, lattice[1], lattice[0]))
        pt1_out.write('{},{},{},{},{}\n'.format(length, lattice[1], lattice[0], gyration[0], gyration[1]))
        pt2_out.write('{},{}\n'.format(length, average_reject_rate))

    pt1_out.close()
    pt2_out.close()
    end_time = time.clock()
    print('Total run time = {:.3f} seconds'.format(end_time - start_time))


main()

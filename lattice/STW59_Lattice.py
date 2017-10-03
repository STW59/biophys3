import gyration as gyr
import latticegen as lat
import pickle


def generate_lattice(length):
    return lat.LatticeGen.generate_lattice(length)


def calc_gyration(length):
    return gyr.Gyration.radius_calc(length)


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
    f = open('STW59_Lattice_Output.txt', 'w')
    f.write('length,conformations,time,min_radius,avg_radius\n')
    for length in range(4, 21):
        lattice = generate_lattice(length)
        # read_data_file(length)
        gyration = calc_gyration(length)

        f.write('{},{},{},{},{}\n'.format(length, lattice[1], lattice[0], gyration[0], gyration[1]))
        print('{},{},{},{},{}\n'.format(length, lattice[1], lattice[0], gyration[0], gyration[1]))
    f.close()


main()

import gyration as gyr
import latticegen as lat
import pickle


def generate_lattice(length):
    print('length = {}'.format(length))
    chain = lat.LatticeGen.generate_lattice(length)
    print('time = {:.9f} seconds'.format(chain))
    print()


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
    for length in range(4, 5):
        generate_lattice(length)
        # read_data_file(length)
        gyr.Gyration.radius_calc(length)

        # TODO: Run from range(4, 17)
        # TODO: Output all data as a csv .txt file


main()

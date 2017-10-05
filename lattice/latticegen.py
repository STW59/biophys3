import os
import pickle
import time


class LatticeGen:
    def __init__(self):
        pass

    @staticmethod
    def initialize_lattice():
        if not os.path.exists('data/'):
            os.mkdir('data/')

        export_file = open('data/lattice_2.dat', 'wb')
        residue_coords = [(0, 0), (0, 1)]
        pickle.dump(residue_coords, export_file)
        export_file.close()

    @staticmethod
    def generate_lattice(chain_length):
        """
        Generates a lattice model given a starting chain length.
        :param chain_length: integer value for the length of the chain
        :return: Elapsed process time
        """
        start_time = time.clock()  # Start performance timer

        conformations = 0
        x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
        y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
        steps = ['u', 'r', 'd', 'l']
        import_file = open('data/lattice_{}.dat'.format(chain_length-1), 'rb')
        export_file = open('data/lattice_{}.dat'.format(chain_length), 'wb')

        try:
            structure = pickle.load(import_file)
            while structure:
                residue_coords = []
                for coords in structure:
                    residue_coords.append(coords)

                x = residue_coords[-1][0]
                y = residue_coords[-1][1]

                for step in steps:
                    residue_coords_iter = residue_coords.copy()
                    x += x_step[step]
                    y += y_step[step]
                    coord = (x, y)
                    if coord not in residue_coords_iter:
                        residue_coords_iter.append(coord)
                        pickle.dump(residue_coords_iter, export_file)
                        conformations += 1

                    x = residue_coords[-1][0]
                    y = residue_coords[-1][1]

                structure = pickle.load(import_file)
        except EOFError:
            pass
        finally:
            import_file.close()
            export_file.close()

        end_time = time.clock()  # End performance timer
        return end_time - start_time, conformations

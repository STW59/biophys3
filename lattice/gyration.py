import numpy as np
import pickle


class Gyration:
    def __init__(self, chain_length):
        self.__chain_length = chain_length

    def chain_length(self):
        return self.__chain_length

    @staticmethod
    def radius_calc(chain_length):
        f = open('data/lattice_{}.dat'.format(chain_length), 'rb')
        rog = []

        try:
            structure = pickle.load(f)
            while structure:
                radius_sum_array = []
                array = np.array(structure)
                avg_coord = np.average(array, axis=0)

                for coords in structure:
                    radius_sum_array.append((coords[0] - avg_coord[0])**2 + (coords[1] - avg_coord[1])**2)
                radius = np.sqrt((1 / len(radius_sum_array)) * sum(radius_sum_array))
                rog.append(radius)

                structure = pickle.load(f)
        except EOFError:
            pass
        finally:
            f.close()
            rog_array = np.array(rog)
            min_radius = np.amin(rog_array)
            avg_radius = np.average(rog_array)

        return min_radius, avg_radius

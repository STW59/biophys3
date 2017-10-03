import numpy as np
import pickle


class Gyration:
    def __init__(self, chain_length):
        self.__chain_length = chain_length

    def chain_length(self):
        return self.__chain_length

    @staticmethod
    def radius_calc(chain_length):
        f = open('lattice_{}.dat'.format(chain_length), 'rb')
        x_sum = 0
        y_sum = 0
        radius_sum = 0
        avg_radius_sum = 0
        min_radius = 1000000
        conformations = 0

        try:
            structure = pickle.load(f)
            while structure:
                for coords in structure:
                    x_sum += coords[0]
                    y_sum += coords[1]
                x_avg = x_sum / chain_length
                y_avg = y_sum / chain_length

                for coords in structure:
                    radius_sum += np.sqrt((coords[0] - x_avg)**2 + (coords[1] - y_avg)**2)
                radius = np.sqrt((1 / chain_length) * radius_sum)
                avg_radius_sum += radius
                if radius < min_radius:
                    min_radius = radius

                conformations += 1
                structure = pickle.load(f)
        except EOFError:
            pass
        finally:
            avg_radius = avg_radius_sum / conformations
            f.close()

        return min_radius, avg_radius

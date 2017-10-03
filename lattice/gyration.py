import numpy as np
import pickle


class Gyration:
    def __init__(self, chain_length):
        self.__chain_length = chain_length

    def chain_length(self):
        return self.__chain_length

    @staticmethod
    def radius_calc(chain_length):
        data = []
        f = open('lattice_{}.dat'.format(chain_length), 'rb')
        try:
            lattice = pickle.load(f)
            while lattice:
                data.append(lattice)
                lattice = pickle.load(f)
        except EOFError:
            pass
        finally:
            f.close()

        # TODO: Calculate radius of gyration for each line
        # TODO: Calculate minimum radius of gyration
        # TODO: Calculate average radius of gyration for each length
        for structure in data:
            for coords in structure:
                print(coords[0])

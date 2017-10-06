import numpy as np


class SimAnneal:
    def __init__(self):
        pass

    @staticmethod
    def anneal():
        beta_start = [1., 5., 9.]
        delta = 0.1

        for betas in beta_start:
            beta = beta_start
            while beta >= 10.0:

                beta = (1 + beta) * delta

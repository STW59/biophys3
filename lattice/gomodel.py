class GoModel:
    def __init__(self):
        pass

    @staticmethod
    def generate_structure():
        # bonds = ['r', 'r', 'r', 'u', 'l', 'l', 'l', 'u', 'u', 'r', 'd', 'r', 'u', 'r', 'd']  # Given structure
        bonds = ['u', 'u', 'u', 'r', 'r', 'r', 'd', 'd', 'd', 'l', 'l', 'u', 'u', 'r', 'd']  # Different test structure
        x = 0
        y = 0
        j = 0
        x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
        y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
        structure = [(x, y)]
        residue_positions = {(x, y): j}
        for bond in bonds:
            j += 1
            x += x_step[bond]
            y += y_step[bond]
            coord = (x, y)
            structure.append(coord)
            residue_positions[(x, y)] = j
        return structure, residue_positions

    @staticmethod
    def calc_energy(structure_data):
        num_contacts = 0
        x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
        y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
        structure = structure_data[0]
        residue_positions = structure_data[1]

        for j in range(len(structure)):
            (x, y) = structure[j]
            partners_list = []
            for direction in ['u', 'r', 'd', 'l']:
                try:
                    k = residue_positions[(x + x_step[direction], y + y_step[direction])]
                    if k > j + 1:
                        partners_list.append(k)
                except KeyError:
                    pass
            partners_list.sort()
            for partner in partners_list:
                num_contacts += 1

        # print('Energy = {} epsilon'.format(-num_contacts))
        return -num_contacts


def main():
    GoModel.calc_energy(GoModel.generate_structure())


# main()

import randomstructure as rs


class GoModel:
    def __init__(self):
        pass

    @staticmethod
    def generate_structure(index):
        if index == 0:
            bonds = ['r', 'r', 'r', 'u', 'l', 'l', 'l', 'u', 'u', 'r', 'd', 'r', 'u', 'r', 'd']  # Given structure
        elif index == 1:
            bonds = ['u', 'u', 'u', 'r', 'd', 'd', 'd', 'r', 'u', 'u', 'u', 'r', 'd', 'd', 'd']  # Different compact structure

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
    # Generate a random structure
    # structure_data = rs.RandomStructure.gen_random_structure(16)

    # Use the pre-defined structure from the assignment
    structure_data = GoModel.generate_structure(0)

    # Calculate the interaction energy for the structure
    energy = GoModel.calc_energy(structure_data)
    print('Model structure interaction energy = {} epsilon'.format(energy))


# main()

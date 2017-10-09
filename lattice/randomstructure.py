import random


class RandomStructure:
    def __init__(self):
        pass

    @staticmethod
    def gen_random_structure(length):
        x_step = {'u': 0, 'r': 1, 'd': 0, 'l': -1}
        y_step = {'u': 1, 'r': 0, 'd': -1, 'l': 0}
        steps = ['u', 'r', 'd', 'l']
        x = 0
        y = 0
        j = 0
        structure = [(x, y)]
        residue_positions = {(x, y): j}

        step = 0
        while step < length - 1:
            j += 1
            coord = (0, 0)
            attempts = 0
            while coord in structure and attempts < 100000:
                x = structure[step][0]
                y = structure[step][1]
                move = steps[random.randint(0, 3)]
                x += x_step[move]
                y += y_step[move]
                coord = (x, y)
                attempts += 1
                # print(coord)

            if attempts < 100000:
                structure.append(coord)
                residue_positions[(x, y)] = j
                step += 1
            elif attempts >= 100000:
                step = 0
                structure = [(x, y)]
                residue_positions = {(x, y): j}

        return structure, residue_positions


def main():
    print(RandomStructure.gen_random_structure(20)[0])


main()

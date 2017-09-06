import numpy as np

FILENAME = "1qcq.pdb"
TABLE1_OUTPUT = "1qcq_t1.txt"
TABLE2_OUTPUT = "1qcq_t2.txt"


def calc_bond_length(r0, r1):
    """
    Calculates bond lengths given two position vectors
    :param r0: position of first atom
    :param r1: position of second atom
    :return: returns bond length
    """
    return np.sqrt((r0[0] - r1[0])**2 + (r0[1] - r1[1])**2 + (r0[2] - r1[2])**2)


def calc_bond_angle(r1, r2, r3):
    """
    Calculates the bond angle (theta) given three position vectors
    :param r1: position of first atom
    :param r2: position of second atom
    :param r3: position of third atom
    :return: returns angle theta
    """
    return 180 - np.degrees(np.arccos(np.dot(r3-r2, r2-r1)/(calc_bond_length(r3, r2) * calc_bond_length(r2, r1))))


def calc_dihedral(r1, r2, r3, r4):
    l1 = r2 - r1
    l2 = r3 - r2
    l3 = r4 - r3
    l1xl2 = np.cross(l1, l2)
    l2xl3 = np.cross(l2, l3)

    if np.dot(l1xl2, l3) < 0:
        sign = -1
    else:
        sign = 1

    return sign * np.degrees(np.arccos(np.dot(l1xl2, l2xl3) /
                                       (np.sqrt(l1xl2[0]**2 + l1xl2[1]**2 + l1xl2[2]**2) *
                                        np.sqrt(l2xl3[0]**2 + l2xl3[1]**2 + l2xl3[2]**2))))


def main():
    # Gather data on all backbone atoms from PDB file
    all_atoms = []

    pdb_file = open(FILENAME, 'r')
    for line in pdb_file:
        if line[0:4] == "ATOM" and line[13:15] in ("N ", "CA", "C "):
            index = int(line[6:11])
            atom = str(line[12:16])  # TODO: Remove spaces from atom string
            residue = str(line[17:20])
            atom_loc = np.array([float(line[30:38]),
                                 float(line[38:46]),
                                 float(line[46:54])])

            atom_data = [index, atom, residue, atom_loc]
            all_atoms.append(atom_data)
    pdb_file.close()

    # Build Table 1
    bonds = []
    angles = []

    # Bond Length Calculation
    bonds.append([1, 'N/A'])
    for n in range(1, len(all_atoms)):
        try:
            atom0 = all_atoms[n - 1]
            atom1 = all_atoms[n]
        except IndexError:
            pass

        bond_length = calc_bond_length(atom0[3], atom1[3])
        bonds.append([atom1[0], bond_length])

    # Theta Calculation
    angles.append([1, 'N/A'])
    for n in range(1, len(all_atoms)):
        try:
            atom0 = all_atoms[n - 1]
            atom1 = all_atoms[n]
            atom2 = all_atoms[n + 1]
        except IndexError:
            angles.append([atom1[0], 'N/A'])
            break

        theta = calc_bond_angle(atom0[3], atom1[3], atom2[3])
        angles.append([atom1[0], theta])

    # t1 = open(TABLE1_OUTPUT, 'w')
    # t1.write('Table 1: Bond Length and Supplemental Bond Angle Theta\n')
    # t1.write('Index,Atom,Bond_Length,Theta\n')
    # for n in range(0, len(bonds)):
    #     t1.write(str(bonds[n][0]) + ',' +
    #              str(all_atoms[n][1]) + ',' +
    #              str(bonds[n][1]) + ',' +
    #              str(angles[n][1]) + '\n')

    # TODO: Make the table columns a consistent width using spaces

    # Build Table 2
    # Calc Phi, Psi, Omega
    print('phi psi omega')
    for n in range(1, len(all_atoms), 3):
        try:
            atom0 = all_atoms[n - 2]
            atom1 = all_atoms[n - 1]
            atom2 = all_atoms[n]
            atom3 = all_atoms[n + 1]
            atom4 = all_atoms[n + 2]
            atom5 = all_atoms[n + 3]
        except IndexError:
            pass

        if n == 1:
            phi = 'N/A'
            psi = calc_dihedral(atom1[3], atom2[3], atom3[3], atom4[3])
            omega = calc_dihedral(atom2[3], atom3[3], atom4[3], atom5[3])
        elif n == len(all_atoms):
            phi = calc_dihedral(atom2[3], atom3[3], atom4[3], atom5[3])
            psi = 'N/A'
            omega = 'N/A'
        else:
            phi = calc_dihedral(atom0[3], atom1[3], atom2[3], atom3[3])
            psi = calc_dihedral(atom1[3], atom2[3], atom3[3], atom4[3])
            omega = calc_dihedral(atom2[3], atom3[3], atom4[3], atom5[3])

        print(phi, psi, omega)

# Table 1: Index, Atom, Bond Length, Bond Angle (theta)
# Table 2: Index, Residue, Phi, Psi, Omega

main()

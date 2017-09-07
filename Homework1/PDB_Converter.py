import numpy as np
import matplotlib.pyplot as plot

"""
1RUZ: 1918 H1 Hemagglutinin
Paper DOI: 10.1126/science.1093155
"""

FILENAME = "1ruz.pdb"
TABLE1_OUTPUT = "1ruz_t1.txt"
TABLE2_OUTPUT = "1ruz_t2.txt"


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
    """
    Calculates the dihedral angle between four position vectors
    :param r1: position of first atom
    :param r2: position of second atom
    :param r3: position of third atom
    :param r4: position of fourth atom
    :return: returns dihedral angle
    """
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
            atom = str(line[13:15])
            if ' ' in atom:
                atom = atom.replace(' ', '')
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
        bonds.append([atom1[0], round(bond_length, 3)])

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
        angles.append([atom1[0], np.around(theta, 3)])

    t1 = open(TABLE1_OUTPUT, 'w')
    t1.write('Table 1: Bond Length and Supplemental Bond Angle Theta\n')
    t1.write('Index  Atom  Bond Length  Theta\n')
    for n in range(0, len(bonds)):
        col_index = str(bonds[n][0]) + '{}'.format(' ' * (7 - len(str(bonds[n][0]))))
        col_atom = str(all_atoms[n][1]) + '{}'.format(' ' * (6 - len(str(all_atoms[n][1]))))
        col_bond_length = str(bonds[n][1]) + '{}'.format(' ' * (13 - len(str(bonds[n][1]))))
        col_theta = str(angles[n][1])
        t1.write(str(col_index) + str(col_atom) + str(col_bond_length) + str(col_theta) + '\n')

    # Build Table 2
    dihedrals = []

    # Calc Phi, Psi, Omega
    index = 1
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
            psi = np.around(calc_dihedral(atom1[3], atom2[3], atom3[3], atom4[3]), 3)
            omega = np.around(calc_dihedral(atom2[3], atom3[3], atom4[3], atom5[3]), 3)
        elif n == len(all_atoms) - 2:
            phi = np.around(calc_dihedral(atom0[3], atom1[3], atom2[3], atom3[3]), 3)
            psi = 'N/A'
            omega = 'N/A'
        else:
            phi = np.around(calc_dihedral(atom0[3], atom1[3], atom2[3], atom3[3]), 3)
            psi = np.around(calc_dihedral(atom1[3], atom2[3], atom3[3], atom4[3]), 3)
            omega = np.around(calc_dihedral(atom2[3], atom3[3], atom4[3], atom5[3]), 3)

        dihedrals.append([index, atom2[2], phi, psi, omega])
        index += 1

# Table 2: Index, Residue, Phi, Psi, Omega
    t2 = open(TABLE2_OUTPUT, 'w')
    t2.write('Table 2: The Three Dihedrals\n')
    t2.write('Index  Residue  Phi       Psi       Omega\n')
    for residue in dihedrals:
        col_index = str(residue[0]) + '{}'.format(' ' * (7 - len(str(residue[0]))))
        col_residue = str(residue[1]) + '{}'.format(' ' * (9 - len(str(residue[1]))))
        col_phi = str(residue[2]) + '{}'.format(' ' * (10 - len(str(residue[2]))))
        col_psi = str(residue[3]) + '{}'.format(' ' * (10 - len(str(residue[3]))))
        col_omega = str(residue[4])
        t2.write(col_index + col_residue + col_phi + col_psi + col_omega + '\n')

    phi_plot = []
    psi_plot = []
    for residue in dihedrals:
        if 'N/A' not in residue:
            phi_plot.append(residue[2])
            psi_plot.append(residue[3])

    fig, ax = plot.subplots()
    ax.scatter(phi_plot, psi_plot)
    ax.set_xlabel(r'$\Phi$ [Degrees]', fontsize=12)
    ax.set_ylabel(r'$\Psi$ [Degrees]', fontsize=12)
    ax.set_title('Ramachandran Plot', fontsize=16)
    ax.set_autoscale_on(False)
    ax.axis([-180, 180, -180, 180])

    ax.grid(True)
    fig.tight_layout()

    plot.show()


main()

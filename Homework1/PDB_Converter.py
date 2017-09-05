import numpy as np

FILENAME = "1qcq.pdb"
TABLE1_OUTPUT = "1qcq_t1.txt"
TABLE2_OUTPUT = "1qcq_t2.txt"


def calc_bond_length(all_atoms):
    atom_n = []
    atom_last = []
    for atom in all_atoms:
        atom_n = atom

        print(atom_n)


def calc_bond_angle(atom1, atom2, atom3):
    pass


def calc_dihedral(atom1, atom2, atom3, atom4):
    pass


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

    bond_length = calc_bond_length(all_atoms)
    # print(bond_length)

    # Calc bond length
    # Calc Theta
    # Calc Phi, Psi, Omega
    # Build Table 1
    # Build Table 2

# Table 1: Index, Atom, Bond Length, Bond Angle (theta)
# Table 2: Index, Residue, Phi, Psi, Omega

main()

# from numpy import *

FILENAME = "1qcq.pdb"
TABLE1_OUTPUT = "1qcq_t1.txt"
TABLE2_OUTPUT = "1qcq_t2.txt"


def main():
    pdb_file = open(FILENAME, 'r')

    for line in pdb_file:
        if line[0:4] == "ATOM" and line[13:15] in ("N ", "CA", "C "):
            print(line.rstrip())  # TEST CODE

    pdb_file.close()

    # Calc bond length
    # Calc Theta
    # Calc Phi, Psi, Omega
    # Build Table 1
    # Build Table 2

# Table 1: Index, Atom, Bond Length, Bond Angle (theta)
# Table 2: Index, Residue, Phi, Psi, Omega

main()

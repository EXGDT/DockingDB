import os
import re


def set_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pdb_path', help='The path which contain your pdb files')
    args = parser.parse_args()
    return args


def use_args(args):
    pdb_path = args.pdb_path
    return pdb_path


def get_pdb_files(pdb_path):
    pdb_files_list = os.listdir(pdb_path)
    pdb_files_list = list((pdb_file for pdb_file in pdb_files_list if 'pdb' in pdb_file))
    return pdb_files_list


def parse_pdb_file(pdb_path, pdb_files_list):
    ion_pdb = []
    mixed_pdb = []
    naked_pdb = []
    single_ligand_pdb = []
    multi_ligand_pdb = []
    big_15000_pdb = []
    UNK_pdb = []
    other_pdb = []
    os.system("mkdir -p ion_pdb")
    os.system("mkdir -p mixed_pdb")
    os.system("mkdir -p naked_pdb")
    os.system("mkdir -p single_ligand_pdb")
    os.system("mkdir -p multi_ligand_pdb")
    os.system("mkdir -p big_15000_pdb")
    os.system("mkdir -p UNK_pdb")
    os.system("mkdir -p other_pdb")
    for file in pdb_files_list:
        file_handle = open('{}/{}'.format(pdb_path, file))
        content = file_handle.readlines()
        het_lines = [line for line in content if re.search("^HET ", line)]
        mod_lines = [line for line in content if re.search("^MODRES ", line)]
        hetnam_lines = [line for line in content if re.search("^HETNAM ", line)]
        ion_lines = [line for line in hetnam_lines if re.search("ION\s*\n", line)]
        atom_lines = [line for line in content if re.search("^ATOM ", line)]
        het_list = []
        mod_list = []
        hetnam_list = []
        ion_list = []
        atom_list = []
        for het_line in het_lines:
            het_list.append(het_line.split()[1])
        for mod_line in mod_lines:
            mod_list.append(mod_line.split()[2])
        for hetnam_line in hetnam_lines:
            hetnam_list.append(hetnam_line.split()[1])
        for ion_line in ion_lines:
            ion_list.append(ion_line.split()[1])
        for atom_line in atom_lines:
            atom_list.append(atom_line.split()[3])
        het_list = list(set(het_list))
        mod_list = list(set(mod_list))
        hetnam_list = list(set(hetnam_list))
        ion_list = list(set(ion_list))
        atom_list = list(set(atom_list))
        if "UNK" in atom_list:
            UNK_pdb.append(file)
            os.system('cp -r {}/{} UNK_pdb'.format(pdb_path, file))
        elif len(atom_lines) >= 15000:
            big_15000_pdb.append(file)
            os.system('cp -r {}/{} big_15000_pdb'.format(pdb_path, file))
        elif len(ion_list) != 0 and len(hetnam_list) - len(mod_list) == len(ion_list):
            ion_pdb.append(file)
            os.system('cp -r {}/{} ion_pdb'.format(pdb_path, file))
        elif len(ion_list) !=0:
            mixed_pdb.append(file)
            os.system('cp -r {}/{} mixed_pdb'.format(pdb_path, file))
        elif len(het_lines) == 0 or len(mod_lines) == len(het_lines):
            naked_pdb.append(file)
            os.system('cp -r {}/{} naked_pdb'.format(pdb_path, file))
        elif len(het_lines) == 1:
            single_ligand_pdb.append(file)
            os.system('cp -r {}/{} single_ligand_pdb'.format(pdb_path, file))
        elif len(het_lines) > 1:
            multi_ligand_pdb.append(file)
            os.system('cp -r {}/{} multi_ligand_pdb'.format(pdb_path, file))
        else:
            other_pdb.append(file)
            os.system('cp -r {}/{} other_pdb'.format(pdb_path, file))
        # content = file_handle.read()
        # if "HETATM" in content:
        #     non_naked_protein.append(file)
        #     os.system('cp -r {}/{} non_naked_pdb/'.format(pdb_path, file))
        # else:
        #     naked_protein.append(file)
        #     os.system('cp -r {}/{} naked_pdb/'.format(pdb_path, file))
    return ion_pdb, mixed_pdb, naked_pdb, single_ligand_pdb, multi_ligand_pdb, big_15000_pdb, UNK_pdb, other_pdb


def get_pdb_name(pdb_file):
    pdb_name = pdb_file.replace('.pdb', '')
    return pdb_name


def main():
    args = set_args()
    pdb_path = use_args(args)
    pdb_files_list = get_pdb_files(pdb_path)
    ion_pdb, mixed_pdb, naked_pdb, single_ligand_pdb, multi_ligand_pdb, big_15000_pdb, UNK_pdb, other_pdb = parse_pdb_file(pdb_path, pdb_files_list)
    print(other_pdb)
    # pdb_name = get_pdb_name(pdb_file)
    # parameters_generate(pdb_name)
    # dock_it(pdb_name)


if __name__ == "__main__":
    main()

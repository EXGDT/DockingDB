import os
import chimera
import AddH
from DockPrep import prep
from WriteDMS import writeDMS
from WriteMol2 import writeMol2
from chimera import runCommand as rc
from chimera import nogui


def set_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pdb_file', help='Your pdb file include path')
    args = parser.parse_args()
    return args


def use_args(args):
    pdb_file = args.pdb_file
    return pdb_file


def get_pdb_files(pdb_path):
    pdb_files_list = os.listdir(pdb_path)
    pdb_files_list = list((pdb_file for pdb_file in pdb_files_list if 'pdb' in pdb_file))
    return pdb_files_list


def get_pdb_name(pdb_file):
    pdb_name = pdb_file.replace('.pdb', '')
    return pdb_name


# def obtain_hetname(pdb_name):
#     file_handle = open('{}.pdb'.format(pdb_name))
#     content = file_handle.readlines()
#     het_lines = [line for line in content if 'HET ' in line]
#     het_list = []
#     for het_line in het_lines:
#         het_list.append(het_line.split()[1])
#     het_list = list(set(het_list))
#     return het_list


# def obtain_ligand_serial(pdb_name):
#     serial_list = []
#     file_handle = open('/public/home/yxguo/test/pdbs_classified/naked_pdb/{}.pdb'.format(pdb_name))
#     content = file_handle.readlines()
#     het_lines = [line for line in content if "HET " in line]
#     for het_line in het_lines:
#         serial_list.append(het_line.split()[3])
#     return serial_list


def edit_rec_sph(pdb_name):
    os.system("mv {}_rec.sph {}_rec.sph.bak".format(pdb_name, pdb_name))
    file_handle = open('{}_rec.sph.bak'.format(pdb_name))
    file_handle2 = open('{}_rec.sph'.format(pdb_name), 'w')
    head = file_handle.readline()
    content = file_handle.readlines()
    for line in content:
        if "cluster     2" in line:
            index_num = content.index(line)
    print(index_num)
    content = content[0:index_num]
    file_handle2.write(head)
    for line in content:
        file_handle2.write(line)
    file_handle.close()
    file_handle2.close()
    print("close handle finished")


def dock_it(pdb_name):
    os.chdir(os.getcwd())
    os.system("mkdir -p {}".format(pdb_name))
    os.chdir("{}".format(pdb_name))
    os.system("cp /home/yxguo/project/DockingDB/pdbs_classified/ion_pdb/{}.pdb ./".format(pdb_name))
    rc("open {}.pdb".format(pdb_name))
    rc("select :/isHet")
    rc("delete sel")
    models = chimera.openModels.list(modelTypes=[chimera.Molecule])
    prep(
        models,
        addHFunc=AddH.hbondAddHydrogens,
        mutateMSE=True,
        mutate5BU=True,
        mutateUMS=True,
        mutateCSL=True,
        delSolvent=True,
        delIons=False,
        delLigands=False,
        nogui=nogui
        )
    writeMol2(models, "{}_rec_charged.mol2".format(pdb_name))
    rc("select H")
    rc("delete sel")
    rc("write format pdb 0 {}_rec_NoH.pdb".format(pdb_name))
    rc("close session")
    insph_file = open('/home/yxguo/project/DockingDB/parameter_files/INSPH')
    insph_out_file = open('INSPH', 'w')
    boxin_file = open('/home/yxguo/project/DockingDB/parameter_files/box.in')
    boxin_out_file = open('box.in', 'w')
    gridin_file = open('/home/yxguo/project/DockingDB/parameter_files/grid.in')
    gridin_out_file = open('grid.in', 'w')
    anchorandgrowin_file = open('/home/yxguo/project/DockingDB/parameter_files/anchor_and_grow.in')
    anchorandgrowin_out_file = open('anchor_and_grow.in', 'w')
    insph_handle = insph_file.read()
    boxin_handle = boxin_file.read()
    gridin_handle = gridin_file.read()
    anchorandgrowin_handle = anchorandgrowin_file.read()
    insph_handle = insph_handle.replace('example.dms', '{}_rec.dms'.format(pdb_name))
    insph_handle = insph_handle.replace('example.sph', '{}_rec.sph'.format(pdb_name))
    boxin_handle = boxin_handle.replace('example.sph', '{}_selected_spheres.sph'.format(pdb_name))
    boxin_handle = boxin_handle.replace('example.pdb', '{}_rec_box.pdb'.format(pdb_name))
    gridin_handle = gridin_handle.replace('example.mol2', '{}_rec_charged.mol2'.format(pdb_name))
    gridin_handle = gridin_handle.replace('example.pdb', '{}_rec_box.pdb'.format(pdb_name))
    gridin_handle = gridin_handle.replace('example', '{}_grid'.format(pdb_name))
    anchorandgrowin_handle = anchorandgrowin_handle.replace('example.mol2', '{}_lig_charged.mol2'.format(pdb_name))
    anchorandgrowin_handle = anchorandgrowin_handle.replace('example_grid', '{}_grid'.format(pdb_name))
    anchorandgrowin_handle = anchorandgrowin_handle.replace('example.sph', '{}_selected_spheres.sph'.format(pdb_name))
    anchorandgrowin_handle = anchorandgrowin_handle.replace('example_output', '{}'.format(pdb_name))
    insph_out_file.write(insph_handle)
    boxin_out_file.write(boxin_handle)
    gridin_out_file.write(gridin_handle)
    anchorandgrowin_out_file.write(anchorandgrowin_handle)
    insph_out_file.close()
    boxin_out_file.close()
    gridin_out_file.close()
    anchorandgrowin_out_file.close()
    
    # rc("open {}.pdb".format(pdb_name))
    # rc("select ligand")
    # rc("select ~sel")
    # rc("delete sel")
    # rc("select :{}".format(serial))
    # rc("select ~sel")
    # rc("delete sel")
    # rc("addh useHisName false")
    # rc("addcharge")
    # models = chimera.openModels.list(modelTypes=[chimera.Molecule])
    # writeMol2(models, "{}_{}_lig_charged.mol2".format(pdb_name, serial))
    # rc("close session")

    rc("open {}_rec_NoH.pdb".format(pdb_name))
    rc("surface")
    surf = chimera.openModels.list(modelTypes=[chimera.MSMSModel])[0]
    writeDMS(surf, "{}_rec.dms".format(pdb_name))
    rc("close session")
    os.system("rm -rf *tmp*")
    os.system("rm -rf *OUTSPH*")
    os.system("rm -rf *rec.sph*")
    os.system("rm -rf *selected_spheres.sph*")
    os.system("rm -rf *rec_box.pdb*")
    os.system("sphgen_cpp")
    edit_rec_sph(pdb_name)
    # sphere_selector_cli = "sphere_selector {}_rec.sph {}_{}_lig_charged.mol2 10.0".format(pdb_name, pdb_name, serial)
    # os.system(sphere_selector_cli)
    os.system("mv {}_rec.sph {}_selected_spheres.sph".format(pdb_name, pdb_name))
    os.system("showbox < box.in")
    os.system("grid -i grid.in")
    # os.system("dock6 -i anchor_and_grow.in")


def main():
    args = set_args()
    pdb_file = use_args(args)
    pdb_name = get_pdb_name(pdb_file)
    dock_it(pdb_name)


if __name__ == "__main__":
    main()

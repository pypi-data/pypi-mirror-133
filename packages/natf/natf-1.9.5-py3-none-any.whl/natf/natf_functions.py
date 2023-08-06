#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import with_statement, print_function
import configparser
import math
import numpy as np
import pandas as pd
import os
from progress.bar import Bar
from natf.mesh import Mesh
from natf.cell import Cell, get_cell_index, is_item_cell
from natf.material import Material, create_pseudo_mat, get_material_index, \
    get_neutron_library_nuclides, is_mat_used
from natf.part import Part, get_part_index_by_name, \
    get_part_index_by_cell_id, is_cell_id_in_parts, is_item_part
from natf.radwaste_standard import RadwasteStandard, rwc_to_int, ctr_to_int
from natf.utils import sgn, time_to_sec, format_single_output, \
    scale_list, is_blank_line, log, get_e_group
from natf.mcnp_input import is_comment, get_cell_cid_mid_den, is_cell_title, \
    cell_title_change_mat, update_mcnp_input_materials, get_tally_numbers, \
    update_mcnp_input_tallies
from natf.mcnp_output import get_cell_tally_info, \
    get_cell_basic_info, get_tbr_from_mcnp_output
from natf.plot import get_rwcs_by_cooling_times, calc_rwc_cooling_requirement, \
    calc_recycle_cooling_requirement
from natf.fispact_input import create_fispact_files, get_fispact_files_template, split_irradiation_scenario, \
    generate_sub_irradiation_files
from natf.fispact_output import read_fispact_out_act, \
    read_fispact_out_sdr, read_fispact_out_dpa, get_interval_list, \
    get_material_after_irradiation
from natf import settings


@log
def get_material_info(mcnp_output):
    """get_material_info, read the mcnp_output file and returns the materials"""

    materials = []
    # read the mcnp_output first time to get the numbers of material
    mat_list = []
    fin = open(mcnp_output)
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError('1cells not found in the file, wrong file!')
        if '1cells' in line:  # read 1cells
            # read the following line
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            while True:
                line = fin.readline()
                if ' total' in line:  # end of the cell information part
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                mid, atom_density, gram_density = int(
                    line_ele[2]), float(
                    line_ele[3]), float(
                    line_ele[4])
                mat_list.append((mid, atom_density, gram_density))
            break
    fin.close()
    mat_list = list(set(mat_list))

    # initial the materials
    for i in range(len(mat_list)):
        m = Material()
        m.id = mat_list[i][0]
        m.atom_density = mat_list[i][1]
        m.density = mat_list[i][2]
        materials.append(m)

    # get the nuclide of the mcnp material
    fin = open(mcnp_output)
    mid = -1
    nuc_list = []
    atom_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, atom fraction' in line:  # read atom fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if 'material' in line:  # end of the material atom fraction part
                    # some materials used only for a perturbation or tally, do not add here
                    if is_mat_used(materials, mid):
                        midx = get_material_index(materials, mid)
                        materials[midx].mcnp_material_nuclide = list(nuc_list)
                        materials[midx].mcnp_material_atom_fraction = scale_list(
                            atom_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        if is_mat_used(materials, mid):
                            midx = get_material_index(materials, mid)
                            materials[midx].mcnp_material_nuclide = list(
                                nuc_list)
                            materials[midx].mcnp_material_atom_fraction = scale_list(
                                atom_fraction_list)
                        nuc_list = []  # reset
                        atom_fraction_list = []  # reset
                    mid = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
            break
    fin.close()

    # get the mass fraction of the nuclide
    fin = open(mcnp_output)
    mid = -1
    nuc_list = []
    mass_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, mass fraction' in line:  # read mass fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if ' warning.' in line or '1cell' in line:  # end of the material atom fraction part
                    if is_mat_used(materials, mid):
                        midx = get_material_index(materials, mid)
                        materials[midx].mcnp_material_nuclide = list(nuc_list)
                        materials[midx].mcnp_material_mass_fraction = scale_list(
                            mass_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        if is_mat_used(materials, mid):
                            midx = get_material_index(materials, mid)
                            materials[midx].mcnp_material_nuclide = list(
                                nuc_list)
                            materials[midx].mcnp_material_mass_fraction = scale_list(
                                mass_fraction_list)
                        nuc_list = []  # reset
                        mass_fraction_list = []  # reset
                    mid = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
            break
    fin.close()
    return materials


@log
def match_cells_materials(cells, materials):
    """match the cells and materials"""
    for c in cells:
        mid = get_material_index(materials, c.mid)
        c.mat = materials[mid]
    return cells


def get_energy_index(energy, energy_group):
    """return energy index according to the energy and energy_group"""
    e_index = -1
    if energy == 'Total':
        return len(energy_group)
    else:
        energy = float(energy)
    for i in range(len(energy_group)):
        if abs(energy - energy_group[i]) / energy_group[i] < 1e-3:
            e_index = i
    if e_index == -1:
        raise ValueError(
            'energy not found in the energy group! Only 175/709 group supported!')
    return e_index


def write_fispact_file(material, irradiation_scenario, model_degree,
                       neutron_flux, file_prefix, tab4flag, endf_lib_flag,
                       fispact_materials, fispact_materials_paths, aim=None,
                       stable_flag=False):
    """
    Write fispact input files: including the input .i the flux .flx files

    Parameters:
    -----------
    material : Material object
        The material to be irradiated
    irradiation_scenario : str
        The filename of the irradiation scenario
    model_degree : float
        The degree of the model used in MCNP. Used to modify the neutron flux by
        a factor of model_degree/360.0
    neutron_flux : numpy array
        The neutron flux (with total)
    file_prefix : str
        The prefix (including the path) of the file
    tab4flag : bool
        Whether to use TAB4 keyword
    endf_lib_flag : bool
        Whether to use ENDF data library
    fispact_materials : list
        The list of the materials that defined by user to use another one
    fispact_materials_paths : list
        The list of the materials paths that need to use
    aim : str
        The AIM of the workflow
    stable_flag : bool
        Whether to show stable nuclides.
    """

    # write the input file
    file_name = f"{file_prefix}.i"
    fo = open(file_name, 'w', encoding='utf-8')
    fo.write('<< ---- get nuclear data ---- >>\n')
    fo.write('NOHEADER\n')
    n_group_size = len(neutron_flux) - 1
    if n_group_size in (709,):
        endf_lib_flag = True
    # endf lib used? ---------
    if endf_lib_flag:
        fo.write('EAFVERSION 8\n')
        fo.write('COVAR\n')
    # ------------------------
    fo.write(f"GETXS 1 {len(neutron_flux) - 1}\n")
    fo.write('GETDECAY 1\n')
    fo.write('FISPACT\n')
    fo.write('* Irradiation start\n')
    fo.write('<< ---- set initial conditions ---- >>\n')
    # material part start
    if aim in ['COOLANT_ACT_PRE']:
        if any(material in sublist for sublist in fispact_materials):
            material_path = settings.get_material_path(fispact_materials,
                                                       fispact_materials_paths, material)
            fo.write(
                '<< ---- material info. defined by user in the separate file below ---- >>\n')
            fo.write(f"<< ---- {material_path} ---->>\n")
            # read the files in fispact_material_list and write it here
            fin = open(material_path)
            for line in fin:
                if line.strip().split() == []:
                    continue
                fo.write(line)
    elif any(material.id in sublist for sublist in fispact_materials):
        material_path = settings.get_material_path(fispact_materials,
                                                   fispact_materials_paths, material.id)
        fo.write(
            '<< ---- material info. defined by user in the separate file below ---- >>\n')
        fo.write(f"<< ---- {material_path} ---- >>\n")
        # read the files in fispact_materials and write it here
        fin = open(material_path)
        for line in fin:
            if line.strip().split() == []:
                continue
            line = line.strip()
            fo.write(f"{line}\n")
    else:
        fo.write('<< ---- material info. converted from MCNP output file ---- >>\n')
        fo.write(f"DENSITY {material.density:.5E}\n")
        fo.write(f'FUEL {len(material.fispact_material_nuclide)}\n')
        for i in range(len(material.fispact_material_nuclide)
                       ):  # write nuclide and atoms information
            fo.write(
                f"{material.fispact_material_nuclide[i]} {material.fispact_material_atoms_kilogram[i]:.5E}\n")
    # material part end
    fo.write('MIND 1.E6\n')
    fo.write('HAZARDS\n')
    if n_group_size in (69, 315):  # fission mode
        fo.write('USEFISSION\n')
        fo.write("FISYIELD 4 Th233 U235 U238 Pu239\n")
    fo.write('CLEAR\n')
    if tab4flag:
        fo.write('TAB4 44\n')
    fo.write('ATWO\n')
    fo.write('HALF\n')
    if not stable_flag:
        fo.write('NOSTABLE\n')
    fo.write('UNCERT 2\n')
    fo.write('TOLERANCE 0 1E4 1.0E-6\n')
    fo.write('TOLERANCE 1 1E4 1.0E-6\n')
    # irradiation scenario part
    if aim == 'COOLANT_ACT_PRE':
        fo.write(irradiation_scenario)
    else:
        with open(irradiation_scenario, 'r', encoding='utf-8') as fin:
            while True:
                line = fin.readline()
                line_ele = line.split()
                if line == '':  # end of the file
                    break
                if is_blank_line(line):
                    continue
                if 'FLUX' in line:  # this is the irradiation part that defines flux
                    try:
                        real_flux = float(
                            line_ele[1]) * model_degree / 360.0 * neutron_flux[n_group_size]
                        fo.write(f"FLUX {real_flux:.5E}\n")
                    except BaseException:
                        errmsg = f"Neutron flux length inconsistency."
                        raise ValueError(errmsg)
                else:
                    fo.write(line)
        # fin.close()
    fo.write('END\n')
    fo.write('*END of RUN \n')
    fo.close()

    # write .flx file
    file_name = f"{file_prefix}.flx"
    fo = open(file_name, 'w')
    for i in range(n_group_size):  # reverse the neutron flux
        fo.write(f"{neutron_flux[n_group_size -1 -i]:.5E}\n")
    fo.write('1.0\n')
    fo.write(
        f"Neutron energy group {n_group_size} G, TOT = {neutron_flux[-1]:.5E}")
    fo.close()


@log
def cell_fispact_cal_pre(
        aim,
        work_dir,
        cells_need_cal,
        model_degree,
        irradiation_scenario,
        fispact_materials,
        fispact_materials_paths,
        fispact_files_dir='',
        fispact_data_dir=None):
    """
    Prepare FISPACT-II input files and FILES

    Parameters:
    -----------
    aim : str
        The AIM of the workflow
    work_dir : str
        The working directory
    cells_need_cal : list of Cell
        The cells need activation calculation
    model_degree : float
        The degree of the model used in MCNP. Used to modify the neutron flux by
        a factor of model_degree/360.0
    irradiation_scenario : str
        The filename of the irradiation scenario
    fispact_materials : list
        The list of the materials that defined by user to use another one
    fispact_materials_paths : list
        The list of the materials paths that need to use
    fispact_files_dir : str
        The directory to story fispact files
    fispact_data_dir : str
        The directory of FISPACT-II data libraries
    """

    if aim not in ('CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST', 'CELL_MAT_EVO'):
        raise RuntimeError('cell_fispact_cal_pre can only called in CELL MODE')
    tab4flag = False
    # endf libaries used, then need keyword EAFVERSION 8
    if aim in ('CELL_DPA_PRE', 'CELL_DPA_POST'):
        endf_lib_flag = True
    else:
        endf_lib_flag = False

    if aim in ('CELL_MAT_EVO'):
        stable_flag = True
    else:
        stable_flag = False

    # create fispact FILES
    if fispact_data_dir:
        n_group_size = len(cells_need_cal[0].neutron_flux) - 1
        tmp_file = get_fispact_files_template(n_group_size)
        filename = create_fispact_files(
            tmp_file, fispact_files_dir=fispact_files_dir, fispact_data_dir=fispact_data_dir)

    for c in cells_need_cal:
        file_prefix = settings.get_fispact_file_prefix(work_dir, c.id,
                                                       fispact_files_dir=fispact_files_dir)
        material = c.mat
        neutron_flux = c.neutron_flux
        try:
            write_fispact_file(
                material,
                irradiation_scenario,
                model_degree,
                neutron_flux,
                file_prefix,
                tab4flag,
                endf_lib_flag,
                fispact_materials,
                fispact_materials_paths,
                stable_flag=stable_flag)
        except BaseException:
            errmsg = f"Encounter error when writing fispact file of cell {c.id}"
            raise ValueError(errmsg)


def construct_irradiation_scenario(irr_time, cooling_times, irr_total_flux):
    """
    Construct FISPACT-II format irradiation scenario.
    """
    irr_snr = '<<-----------Irradiation Scenario--------------->>\n'
    irr_snr += 'FLUX ' + format_single_output(irr_total_flux) + '\n'
    irr_snr += 'TIME ' + format_single_output(irr_time) + ' SECS ATOMS\n'
    irr_snr += 'ZERO\n'
    irr_snr += '<<-----------End of Irradiation --------------->>\n'
    irr_snr += '<<-----------Cooling Times--------------->>\n'
    for i, ct in enumerate(cooling_times):
        irr_snr += 'TIME ' + format_single_output(ct) + ' SECS ATOMS\n'
    return irr_snr


def calc_part_irradiation_scenario(part_name, coolant_flow_parameters,
                                   flux_multiplier, n_total_flux, model_degree=360.0):
    """
    Calculate the irradiation scenario according to the coolant flow parameters.

    Parameters:
    -----------
    part_name: str
        The name of the part.
    coolant_flow_parameters: str
        The file path of the coolant flow parameters.
    flux_multiplier: float
        The total neutron emitting rate of the fusion device.
        Eg: for CFETR 200 MW case, the value is 7.09e19.
    n_total_flux: float
        Total flux of the part.equal_cell.
    model_degree: float
        Default 360.

    Returns:
    --------
    irradiation_scenario: str
    """
    irr_time, cooling_times = settings.get_irr_and_cooling_times(
        part_name, coolant_flow_parameters)
    irr_total_flux = model_degree / 360.0 * flux_multiplier * n_total_flux
    irradiation_scenario = construct_irradiation_scenario(
        irr_time, cooling_times, irr_total_flux)
    return irradiation_scenario


@log
def parts_fispact_cal_pre(aim, work_dir, parts, model_degree,
                          fispact_materials, fispact_materials_paths, coolant_flow_parameters,
                          flux_multiplier, fispact_files_dir=''):
    """fispact_cal_pre, write .flx and .i files for fispact according to the aim"""
    tab4flag = False
    endf_lib_flag = False
    # endf libaries used, then need keyword EAFVERSION 8 for p in parts:
    for p in parts:
        file_prefix = settings.get_fispact_file_prefix(work_dir, ele_id=p.name,
                                                       ele_type='p', fispact_files_dir=fispact_files_dir)
        neutron_flux = p.equal_cell.neutron_flux
        material = p.equal_cell.name
        irradiation_scenario = calc_part_irradiation_scenario(p.name,
                                                              coolant_flow_parameters, flux_multiplier, p.equal_cell.neutron_flux[-1], model_degree)
        try:
            write_fispact_file(material, irradiation_scenario, model_degree,
                               neutron_flux, file_prefix, tab4flag, endf_lib_flag,
                               fispact_materials, fispact_materials_paths, aim=aim)
        except BaseException:
            errmsg = f"Error when writing fispact file of part {p.name}"
            raise ValueError(errmsg)


@log
def read_fispact_output_cell(cells_need_cal, work_dir, aim, cooling_times_cul,
                             fispact_files_dir=''):
    """read_fispact_output_act: read the fispact output file to get activation information of cells
    input: cells_need_cal, list a cells that need to calculate and analysis
    input: work_dir, the working director
    return: cells_need_cal, changed list of cells"""
    interval_list = settings.check_interval_list(
        cells_need_cal, work_dir, fispact_files_dir=fispact_files_dir)
    print('     the intervals need to read are {0}'.format(interval_list))
    bar = Bar("reading fispact output files", max=len(
        cells_need_cal), suffix='%(percent).1f%% - %(eta)ds')
    for c in cells_need_cal:
        file_prefix = settings.get_fispact_file_prefix(work_dir, ele_id=c.id,
                                                       ele_type='c', fispact_files_dir=fispact_files_dir)
        filename = f"{file_prefix}.out"
        if aim in ('CELL_ACT_POST'):  # read output information
            read_fispact_out_act(c, filename, interval_list)
        if aim == 'CELL_DPA_POST':  # read DPA information
            read_fispact_out_act(c, filename, interval_list)
            read_fispact_out_dpa(c, filename, interval_list)
        bar.next()
    bar.finish()


@log
def read_fispact_output_part(parts, work_dir, aim, fispact_files_dir=''):
    """read_fispact_output_part: read the fispact output file to get
    activation information of parts in PHTS.

    Parameters:
    -----------
    parts:  list of parts
        parts that need to calculate and analysis
    work_dir: string
        The working director

    Returns:
    --------
    parts:
        Changed list of parts
    """
    interval_list = settings.check_interval_list(
        parts, work_dir, fispact_files_dir=fispact_files_dir)
    print('     the intervals need to read are {0}'.format(interval_list))
    for i, p in enumerate(parts):
        print('       reading part {0} start'.format(p.name))
        if aim == 'COOLANT_ACT_POST':  # read output information
            file_prefix = settings.get_fispact_file_prefix(work_dir, ele_id=p.name,
                                                           ele_type='p', fispact_files_dir=fispact_files_dir)
            filename = f"{file_prefix}.out"
            read_fispact_out_act(p.equal_cell, filename, interval_list)
            read_fispact_out_sdr(p.equal_cell, filename, interval_list)


@log
def cell_act_post_process(parts, work_dir, model_degree, aim,
                          cooling_times_cul, rwss=[]):
    """
    cell_act_post_process: treat the parts, analysis the data and output results

    Parameters:
    -----------
    ...
    rwss: list of RadwasteStandard, optional
        Radwaste standards used.
    """
    # first, merge the cells in the part to get the equal_cell
    if aim in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        bar = Bar(f"merging cells of each part", max=len(
            parts), suffix='%(percent).1f%% - %(eta)ds')
        for p in parts:
            p.merge_cell(aim)
            bar.next()
        bar.finish()

    # if the aim is CELL_ACT_POST, then there should perform analysis
    if aim == 'CELL_ACT_POST':
        bar = Bar(f"analysis radwaste of parts", max=len(
            parts), suffix='%(percent).1f%% - %(eta)ds')
        for p in parts:
            p.part_act_analysis(aim, rwss=rwss)
            bar.next()
        bar.finish()

    # if the aim is CELL_DPA_POST, don't do anything
    # output the data
    bar = Bar(f"output results", max=len(parts),
              suffix='%(percent).1f%% - %(eta)ds')
    for p in parts:
        p.output_data(work_dir, model_degree, aim,
                      cooling_times_cul=cooling_times_cul, rwss=rwss)
        bar.next()
    bar.finish()


def coolant_act_post_process(parts, nodes, work_dir, model_degree, aim):
    """
    coolant_act_post_process: treat the parts and coolant, analysis the data
    and output results
    """
    # merge nodes data
    for i, node in enumerate(nodes):
        settings.merge_node_parts(node, parts, i)

    # output the data
    for p in parts:
        p.output_data(work_dir, model_degree, aim)
    for node in nodes:
        node.output_data(work_dir, model_degree, aim)


@log
def treat_nuc_responses(cells, parts, nuc_treatment):
    """
    Treat the nuclide in cells. Such as extract the H3 by a factor of 99.9%.
    """
    if nuc_treatment == '':
        return cells
    item_nuc_treatments = settings.get_item_nuc_treatments(nuc_treatment)
    item_nuc_treatments = settings.expand_item_nuc_treatments(
        item_nuc_treatments, cells, parts)
    bar = Bar("treating nuclides responses", max=len(
        item_nuc_treatments), suffix='%(percent).1f%% - %(eta)ds')
    for i, cnt in enumerate(item_nuc_treatments):
        cidx = get_cell_index(cells, cnt[0])  # find cell index
        cells[cidx].treat_nuc_responses(cnt[1], cnt[2])
        bar.next()
    bar.finish()
    return cells


def natf_cell_rwc_vis(config):
    """
    Modify the mcnp_input for visualization.
    """
    # ------ READ input -------
    aim = 'CELL_RWC_VIS'
    work_dir = config.get('general', 'work_dir', fallback='.')
    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)
    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')
    cells = get_cell_basic_info(mcnp_output)
    cells = get_cell_tally_info(mcnp_output, cells, tally_number, n_group_size,
                                continue_output=continue_output)
    # [model], required
    part_cell_list = os.path.join(
        work_dir, config.get('model', 'part_cell_list'))
    parts = settings.get_part(cells, part_cell_list)
    # [fispact]
    irradiation_scenario = os.path.join(work_dir,
                                        config.get('fispact', 'irradiation_scenario'))
    cooling_times = settings.get_cooling_times(irradiation_scenario, aim)
    cooling_times_cul = settings.get_cooling_times_cul(cooling_times)
    # [radwaste] standard
    rwss = settings.get_radwaste_standards(config)

    # get RWC CHN2018 for each cooling_time
    names = []
    for p in parts:
        names.append(p.name)
    # rewrite mcnp_input for each cooling_time
    for rws in rwss:
        key = f'rwc_{rws.standard.lower()}'
        rwcs = get_rwcs_by_cooling_times(names, cooling_times=cooling_times_cul,
                                         key=key, work_dir=work_dir)
        if rws.standard in ['CHN2018']:
            classes = ['LLW', 'Clearance']
        else:
            classes = ['LLW']

        ctrs = calc_rwc_cooling_requirement(names, key=key,
                                            classes=classes, standard=rws.standard, work_dir=work_dir,
                                            out_unit='a', ofname=None)
        for i, ct in enumerate(cooling_times_cul):
            filename = f"{mcnp_input}_{rws.standard.lower()}_ct{i}.txt"
            fo = open(filename, 'w')
            # rewrite cell card
            with open(mcnp_input, 'r') as fin:
                cell_start, surf_start = False, False
                cell_end, surf_end = False, False
                while True:
                    line = fin.readline()
                    if line == '':
                        break
                    # end of cell card
                    if is_blank_line(line) and cell_start and not surf_start:
                        cell_end = True
                        surf_start = True
                        fo.write(line)
                        continue
                    if is_comment(line):
                        fo.write(line)
                        continue
                    if is_cell_title(line):
                        cell_start = True
                        cid, mid, den = get_cell_cid_mid_den(line)
                        if is_cell_id_in_parts(parts, cid):
                            pidx = get_part_index_by_cell_id(
                                parts, cid, find_last=True)
                            rwc = rwcs[pidx][i]
                            rwci = rwc_to_int(rwc, standard=rws.standard)
                            new_line = cell_title_change_mat(
                                line, mid_new=rwci, den_new=1.0)
                            fo.write(new_line+'\n')
                        else:  # this cell do not belong to activated parts, set to void
                            new_line = cell_title_change_mat(
                                line, mid_new=0, den_new=None)
                            fo.write(new_line+'\n')
                        continue
                    if is_blank_line(line) and surf_start and not surf_end:
                        surf_end = True
                        fo.write(line)
                        # append pseudo-mat here
                        fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                        fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                        continue
                    fo.write(line)  # other lines
            fo.write('\n')  # new line at the end
            fo.close()
        # rewrite mcnp_input for Time-to-Clearance and Time-to-LLW
        for i, cls in enumerate(classes):
            filename = f"{mcnp_input}_{rws.standard.lower()}_to_{cls}.txt"
            fo = open(filename, 'w')
            # rewrite cell card
            with open(mcnp_input, 'r') as fin:
                cell_start, surf_start = False, False
                cell_end, surf_end = False, False
                while True:
                    line = fin.readline()
                    if line == '':
                        break
                    # end of cell card
                    if is_blank_line(line) and cell_start and not surf_start:
                        cell_end = True
                        surf_start = True
                        fo.write(line)
                        continue
                    if is_comment(line):
                        fo.write(line)
                        continue
                    if is_cell_title(line):
                        cell_start = True
                        cid, mid, den = get_cell_cid_mid_den(line)
                        if is_cell_id_in_parts(parts, cid):
                            pidx = get_part_index_by_cell_id(
                                parts, cid, find_last=True)
                            ctr = ctrs[pidx][i]
                            ctri = ctr_to_int(ctr)
                            new_line = cell_title_change_mat(
                                line, mid_new=ctri, den_new=1.0)
                            fo.write(new_line+'\n')
                            continue
                        else:  # this cell do not belong to activated parts, set to void
                            new_line = cell_title_change_mat(
                                line, mid_new=0, den_new=None)
                            fo.write(new_line+'\n')
                            continue
                    if is_blank_line(line) and surf_start and not surf_end:
                        surf_end = True
                        fo.write(line)
                        # append pseudo-mat here
                        fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                        fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                        fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                        continue
                    fo.write(line)  # other lines
            fo.write('\n')  # new line at the end
            fo.close()
    # rewrite mcnp_input for Recycling
    ctrs = [[], []]  # CRH, ARH
    ctrs[0] = calc_recycle_cooling_requirement(
        names, key='cdt', rh='CRH', work_dir=work_dir, out_unit='a')
    ctrs[1] = calc_recycle_cooling_requirement(
        names, key='cdt', rh='ARH', work_dir=work_dir, out_unit='a')
    for i in range(0, 2):
        if i == 0:
            filename = f"{mcnp_input}_to_recycle_crh.txt"
        else:
            filename = f"{mcnp_input}_to_recycle_arh.txt"
        fo = open(filename, 'w')
        # rewrite cell card
        with open(mcnp_input, 'r') as fin:
            cell_start, surf_start = False, False
            cell_end, surf_end = False, False
            while True:
                line = fin.readline()
                if line == '':
                    break
                if is_blank_line(line) and cell_start and not surf_start:  # end of cell card
                    cell_end = True
                    surf_start = True
                    fo.write(line)
                    continue
                if is_comment(line):
                    fo.write(line)
                    continue
                if is_cell_title(line):
                    cell_start = True
                    cid, mid, den = get_cell_cid_mid_den(line)
                    if is_cell_id_in_parts(parts, cid):
                        pidx = get_part_index_by_cell_id(
                            parts, cid, find_last=True)
                        ctrs
                        ctr = ctrs[i][pidx]
                        ctri = ctr_to_int(ctr)
                        new_line = cell_title_change_mat(
                            line, mid_new=ctri, den_new=1.0)
                        fo.write(new_line+'\n')
                        continue
                    else:  # this cell do not belong to activated parts, set to void
                        new_line = cell_title_change_mat(
                            line, mid_new=0, den_new=None)
                        fo.write(new_line+'\n')
                        continue
                if is_blank_line(line) and surf_start and not surf_end:
                    surf_end = True
                    fo.write(line)
                    # append pseudo-mat here
                    fo.write(f"C ---- pseudo-mat for RWC VIS--------\n")
                    fo.write(create_pseudo_mat(mid=1).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=2).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=3).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=4).__str__()+'\n')
                    fo.write(create_pseudo_mat(mid=5).__str__()+'\n')
                    continue
                fo.write(line)  # other lines
        fo.write('\n')  # new line at the end
        fo.close()
    print(f'NATF: {aim} completed!\n')


def natf_cell_act_pre(config):
    # general
    work_dir = config.get('general', 'work_dir', fallback='.')
    aim = config.get('general', 'aim')
    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)
    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')

    # [fispact]
    # fispact.fispact_materials, optional
    fispact_material_list = config.get(
        'fispact', 'fispact_material_list', fallback='')
    if fispact_material_list != '':
        FISACT_MATERIAL_LIST = os.path.join(
            work_dir, fispact_material_list)
    # fispact.irradiation_scenario
    irradiation_scenario = os.path.join(
        work_dir, config.get('fispact', 'irradiation_scenario'))
    # fispact.fispact_files_dir, optional
    fispact_files_dir = config.get('fispact', 'fispact_files_dir', fallback='')
    if fispact_files_dir != '':
        fispact_files_dir = os.path.join(work_dir, fispact_files_dir)
    fispact_data_dir = settings.get_fispact_data_dir(config)

    # [model], required
    part_cell_list = os.path.join(
        work_dir, config.get('model', 'part_cell_list'))
    # model.model_degree, optional
    model_degree = float(config.get('model', 'model_degree', fallback=360.0))

    # read the fispact material list
    fispact_materials, fispact_materials_paths = settings.get_fispact_materials(
        fispact_material_list, aim)
    cooling_times = settings.get_cooling_times(irradiation_scenario, aim)
    cooling_times_cul = settings.get_cooling_times_cul(cooling_times)
    # read mcnp output file, get cell information:
    # icl, cid, mid, vol (cm3), mass (g)
    cells = get_cell_basic_info(mcnp_output)
    cells = get_cell_tally_info(mcnp_output, cells, tally_number, n_group_size,
                                continue_output=continue_output)
    materials = get_material_info(mcnp_output)
    for mat in materials:
        mat.mcnp2fispact()
    cells = match_cells_materials(cells, materials)
    parts = settings.get_part(cells, part_cell_list)
    cells_need_cal = settings.get_cell_need_cal(aim, parts, cells)
    cell_fispact_cal_pre(aim, work_dir, cells_need_cal, model_degree,
                         irradiation_scenario, fispact_materials,
                         fispact_materials_paths,
                         fispact_files_dir=fispact_files_dir,
                         fispact_data_dir=fispact_data_dir)
    # generate FISPACT FILES and fisprun.sh

    print(f'NATF: {aim} completed!\n')


def natf_cell_act_post(config):
    # general
    work_dir = config.get('general', 'work_dir', fallback='.')
    aim = config.get('general', 'aim')
    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)
    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')

    # [fispact]
    # fispact.irradiation_scenario
    irradiation_scenario = os.path.join(
        work_dir, config.get('fispact', 'irradiation_scenario'))
    # nuc treatment
    nuc_treatment = config.get('fispact', 'nuc_treatment', fallback='')
    # fispact.fispact_files_dir, optional
    fispact_files_dir = config.get('fispact', 'fispact_files_dir', fallback='')
    if fispact_files_dir != '':
        fispact_files_dir = os.path.join(work_dir, fispact_files_dir)

    # [model], required
    part_cell_list = os.path.join(
        work_dir, config.get('model', 'part_cell_list'))
    # model.model_degree, optional
    model_degree = float(config.get('model', 'model_degree', fallback=360.0))

    # [radwaste] standard
    rwss = settings.get_radwaste_standards(config)

    # get the cooling times
    cooling_times = settings.get_cooling_times(irradiation_scenario, aim)
    cooling_times_cul = settings.get_cooling_times_cul(cooling_times)

    # read mcnp output file, get cell information:
    # icl, cid, mid, vol (cm3), mass (g)
    cells = get_cell_basic_info(mcnp_output)
    cells = get_cell_tally_info(mcnp_output, cells, tally_number, n_group_size,
                                continue_output=continue_output)
    materials = get_material_info(mcnp_output)
    for mat in materials:
        mat.mcnp2fispact()
    cells = match_cells_materials(cells, materials)
    parts = settings.get_part(cells, part_cell_list)
    cells_need_cal = settings.get_cell_need_cal(aim, parts, cells)

    # deal with the fispact output and data analysis
    # first, check whether all the fispact output files are available
    settings.check_fispact_output_files(
        cells_need_cal, work_dir, aim, fispact_files_dir=fispact_files_dir)
    # then read the output information
    read_fispact_output_cell(cells_need_cal, work_dir, aim,
                             cooling_times_cul, fispact_files_dir=fispact_files_dir)
    treat_nuc_responses(cells_need_cal, parts, nuc_treatment)
    cell_act_post_process(parts, work_dir, model_degree,
                          aim, cooling_times_cul, rwss=rwss)
    print(f'NATF: {aim} completed!\n')


def natf_coolant_act_pre(config):
    # [general]
    work_dir = config.get('general', 'work_dir', fallback='.')
    aim = config.get('general', 'aim')
    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)

    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')

    # [coolant_flow]
    coolant_flow_parameters = os.path.join(work_dir,
                                           config.get('coolant_flow', 'coolant_flow_parameters'))
    flux_multiplier = float(config.get('coolant_flow', 'flux_multiplier'))

    # [fispact]
    # fispact.fispact_material_list, optional
    fispact_material_list = config.get(
        'fispact', 'fispact_material_list', fallback='')
    if fispact_material_list != '':
        FISACT_MATERIAL_LIST = os.path.join(
            work_dir, fispact_material_list)

    # fispact.fispact_files_dir, optional
    fispact_files_dir = config.get('fispact', 'fispact_files_dir', fallback='')
    if fispact_files_dir != '':
        fispact_files_dir = os.path.join(work_dir, fispact_files_dir)

    # [model], required
    part_cell_list = os.path.join(work_dir,
                                  config.get('model', 'part_cell_list'))
    # model.model_degree, optional
    model_degree = float(config.get('model', 'model_degree', fallback=360.0))

    # read the fispact material list
    fispact_materials, fispact_materials_paths = settings.get_fispact_materials(
        fispact_material_list, aim)

    cells = get_cell_basic_info(mcnp_output)
    cells = get_cell_tally_info(
        mcnp_output, cells, tally_number, n_group_size)
    parts = settings.get_part(cells, part_cell_list, coolant_flow_parameters)
    nodes = settings.get_nodes(coolant_flow_parameters)
    parts_fispact_cal_pre(aim, work_dir, parts, model_degree,
                          fispact_materials, fispact_materials_paths,
                          coolant_flow_parameters, flux_multiplier)
    print(f'NATF: {aim} completed!\n')


def natf_coolant_act_post(config):
    # general
    work_dir = config.get('general', 'work_dir', fallback='.')
    aim = config.get('general', 'aim')

    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)
    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')

    # [coolant_flow]
    coolant_flow_parameters = os.path.join(work_dir,
                                           config.get('coolant_flow', 'coolant_flow_parameters'))
    flux_multiplier = float(config.get('coolant_flow', 'flux_multiplier'))

    # [fispact]
    # fispact.fispact_material_list, optional
    fispact_material_list = config.get(
        'fispact', 'fispact_material_list', fallback='')
    if fispact_material_list != '':
        FISACT_MATERIAL_LIST = os.path.join(
            work_dir, fispact_material_list)

    # fispact.fispact_files_dir, optional
    fispact_files_dir = config.get('fispact', 'fispact_files_dir', fallback='')
    if fispact_files_dir != '':
        fispact_files_dir = os.path.join(work_dir, fispact_files_dir)

    # [model], required
    part_cell_list = os.path.join(work_dir,
                                  config.get('model', 'part_cell_list'))
    # model.model_degree, optional
    model_degree = float(config.get('model', 'model_degree', fallback=360.0))

    # read the fispact material list
    fispact_materials, fispact_materials_paths = settings.get_fispact_materials(
        fispact_material_list, aim)

    cells = get_cell_basic_info(mcnp_output)
    cells = get_cell_tally_info(
        mcnp_output, cells, tally_number, n_group_size)
    parts = settings.get_part(cells, part_cell_list, coolant_flow_parameters)
    nodes = settings.get_nodes(coolant_flow_parameters)

    # check whether all the fispact output files are available
    settings.check_fispact_output_files(
        parts, work_dir, aim, fispact_files_dir=fispact_files_dir)
    read_fispact_output_part(parts, work_dir, aim,
                             fispact_files_dir=fispact_files_dir)
    coolant_act_post_process(parts, nodes, work_dir, model_degree, aim)
    print(f'NATF: {aim} completed!\n')


def natf_cell_mat_evo(config):
    """
    Monte Carlo and activation coupling calculation. The material will be
    updated at each time step.

    Required inputs:
        - mcnp_input: mcnp input file
        - mcnp_output: mcnp output file

    workflow:
        1. generate fispact input file from information provide in mcnp
           input/output and irradiation history/time step.
           Only irradiation is performed if it's not the last time step.
           Both irradiation and cooling is performed if it's last time step.
        2. read fispact output file and get the updated material compositon,
           write a new mcnp input file
        3. goto step 1 if the time step is not finished, or goto step 4 if
           it's last time step
        4. perform CELL_ACT_POST with the mcnp output and fispact output. 
    """

    # ============= reading parameters from input
    # [general]
    work_dir = config.get('general', 'work_dir', fallback='.')
    aim = config.get('general', 'aim')

    # [mcnp]
    mcnp_input = os.path.join(work_dir, config.get('mcnp', 'mcnp_input'))
    mcnp_output = os.path.join(work_dir, config.get('mcnp', 'mcnp_output'))
    continue_output = config.get('mcnp', 'continue_output', fallback='')
    if continue_output:
        continue_output = os.path.join(work_dir, continue_output)
    # mcnp.tally_number
    tally_number = settings.get_tally_number(config)
    # mcnp.n_group_size
    n_group_size = config.getint('mcnp', 'n_group_size')
    # mcnp.nuclide_sets
    nuclide_sets = settings.get_nuclide_sets(config)

    # [fispact]
    # fispact.irradiation_scenario, required in CELL_ACT and CELL_DPA mode
    irradiation_scenario = config.get('fispact', 'irradiation_scenario')
    # fispact.fispact_files_dir
    # required becuase large amout of files will be generated for each time step
    fispact_files_dir = config.get('fispact', 'fispact_files_dir')
    if fispact_files_dir != '':
        fispact_files_dir = os.path.join(work_dir, fispact_files_dir)
    fispact_data_dir = settings.get_fispact_data_dir(config)
    # fispact.nuc_treatment, optional
    try:
        nuc_treatment = config.get('fispact', 'nuc_treatment')
        if nuc_treatment != '':
            nuc_treatment = os.path.join(work_dir, nuc_treatment)
    except:
        nuc_treatment = ''
    # fispact.time_step, required, unit: MWY
    power_time_step = float(config.get('fispact', 'power_time_step'))
    # create folder to store temporary files for each step
    dump_dir = 'DUMP_FILES'
    dump_dir = os.path.join(work_dir, dump_dir)
    if not os.path.isdir(dump_dir):
        os.system(f"mkdir -pv {dump_dir}")

    # [model], required
    part_cell_list = os.path.join(
        work_dir, config.get('model', 'part_cell_list'))
    # model.model_degree, optional
    model_degree = float(config.get('model', 'model_degree', fallback=360.0))

    # [debug], optional
    monitor_cells = settings.get_monitor_cells(config)
    print(f"    cell: {monitor_cells} are monitored for dropped nuclides")
    monitor_nucs = settings.get_monitor_nucs(config)
    print(
        f"    nucs: {monitor_nucs} are monitored for inventory vs. iteration")

    # ============= PREPARE start ================
    # check and update status of the workflow
    status_file = 'status.ini'
    irrad_blocks, operation_times = split_irradiation_scenario(
        irradiation_scenario, power_time_step)
    total_steps = len(irrad_blocks)
    current_step = 0
    stat = 'PRE'
    if os.path.isfile(status_file):
        total_steps, current_step, stat = settings.read_mat_evo_status(
            status_file)
    else:  # it is step0 pre if the status file does not exist
        # split irradiation scenario
        generate_sub_irradiation_files(irrad_blocks, dump_dir)
        settings.update_mat_evo_status(
            status_file, total_steps, current_step, stat)

    # Record imporant parameters and values along with iteration
    # init tbr.csv
    tbr_file = 'tbr.csv'
    if current_step == 0:
        with open(tbr_file, 'w') as fo:
            fo.write("Operation time (MWY),TBR\n")
    # dropped nuclides
    record_file_total = None
    record_file_total = f"monitored_cells_nuc_drop.csv"
    if monitor_cells and current_step == 0:
        with open(record_file_total, 'w') as fo:
            fo.write("Iteration step,Dropped atoms (atoms/kg)\n")
    # inventory of specific nuclide
    monitor_nucs_file = f"monitored_nucs_inventory.csv"
    if monitor_nucs and current_step == 0:
        cnt = 'Iteration step'
        for nuc in monitor_nucs:
            cnt = f"{cnt},{nuc}(atoms),{nuc}(grams)"
        with open(monitor_nucs_file, 'w') as fo:
            fo.write(f"{cnt}\n")
    # ============= PREPARE end ================

    # ============= step 1 start ===============
    if current_step > 0:
        mcnp_output = os.path.join(dump_dir, f"step{current_step}", "outp")
        continue_output = os.path.join(dump_dir, f"step{current_step}", "outq")
    step_dir = os.path.join(dump_dir, f"step{current_step}")
    fispact_files_dir = os.path.join(
        step_dir, fispact_files_dir.split("/")[-1])
    if not os.path.exists(fispact_files_dir):
        os.system(f"mkdir -p {fispact_files_dir}")
    irradiation_scenario = os.path.join(step_dir, "irradiation_scenario")

    if stat == 'PRE':
        # redirect some file to STEP i
        # read the fispact material list
        # mat replacement is not allowed in CELL_MAT_EVO mode
        fispact_materials, fispact_materials_paths = [], []
        # read mcnp output file, get cell information:
        # icl, cid, mid, vol (cm3), mass (g)
        cells = get_cell_basic_info(mcnp_output)
        cells = get_cell_tally_info(mcnp_output, cells, tally_number, n_group_size,
                                    continue_output=continue_output)
        materials = get_material_info(mcnp_output)
        for mat in materials:
            mat.mcnp2fispact()
        cells = match_cells_materials(cells, materials)
        parts = settings.get_part(cells, part_cell_list)
        cells_need_cal = settings.get_cell_need_cal(aim, parts, cells)
        cell_fispact_cal_pre(aim, work_dir, cells_need_cal, model_degree,
                             irradiation_scenario, fispact_materials,
                             fispact_materials_paths,
                             fispact_files_dir=fispact_files_dir,
                             fispact_data_dir=fispact_data_dir)
        if current_step > 0:
            tally_numbers = get_tally_numbers(mcnp_input)
            tbr_tallies = update_mcnp_input_tallies(
                mcnp_input, cells_need_cal, tid_start=max(tally_numbers), write_file=False)
            tbr = get_tbr_from_mcnp_output(mcnp_output, tbr_tallies)
            settings.update_tbr_file(
                tbr_file, operation_times[current_step-1], tbr)
        settings.update_mat_evo_status(
            status_file, total_steps, current_step, 'POST')
        print(f"End of NATF {aim}, step {current_step}, {stat}")
    # ============= step 1 end   ===============

    # ============= step 2 start ================
    if stat == 'POST':
        # read mcnp output file, get cell information:
        # icl, cid, mid, vol (cm3), mass (g)
        cells = get_cell_basic_info(mcnp_output)
        cells = get_cell_tally_info(mcnp_output, cells, tally_number, n_group_size,
                                    continue_output=continue_output)
        parts = settings.get_part(cells, part_cell_list)
        cells_need_cal = settings.get_cell_need_cal(aim, parts, cells)
        # check whether all the fispact output files are available
        settings.check_fispact_output_files(
            cells_need_cal, work_dir, aim, fispact_files_dir=fispact_files_dir)

        # update the material after irradiation
        mids = []
        for c in cells:
            mids.append(c.mid)
        mid_max = max(mids)
        current_mid = max(mid_max, 10000) + 1
        ntrans_avail_nucs = get_neutron_library_nuclides(
            nuclide_sets=nuclide_sets)
        item_nuc_treatments = settings.get_item_nuc_treatments(nuc_treatment)
        item_nuc_treatments = settings.expand_item_nuc_treatments(
            item_nuc_treatments, cells, parts)
        nucs_to_treat = settings.get_nucs_to_treat(item_nuc_treatments)
        total_dropped_atoms = 0.0
        monitor_nucs_atoms = [0.0]*len(monitor_nucs)
        monitor_nucs_grams = [0.0]*len(monitor_nucs)
        purified_atoms = [0.0]*len(nucs_to_treat)
        purified_grams = [0.0]*len(nucs_to_treat)
        for c in cells_need_cal:
            c_ofname = os.path.join(fispact_files_dir, f"c{c.id}.out")
            mat = get_material_after_irradiation(c_ofname, current_mid)
            # treat the fispact output nuc composition
            for i, cnl in enumerate(item_nuc_treatments):
                if item_nuc_treatments[i][0] == c.id:
                    pur_atoms, pur_grams = mat.treat_fispact_nuc_composition(
                        nuc=cnl[1], level=cnl[2])
                    nidx = nucs_to_treat.index(cnl[1])
                    purified_atoms[nidx] += pur_atoms * c.mass/1e3
                    purified_grams[nidx] += pur_grams * c.mass/1e3
            # monitor nucs
            for i, nuc in enumerate(monitor_nucs):
                nidx = mat.fispact_material_nuclide.index(nuc)
                nuc_atoms = mat.fispact_material_atoms_kilogram[nidx] * c.mass/1e3
                monitor_nucs_atoms[i] += nuc_atoms
                nuc_grams = mat._fispact_material_grams_kilogram[nidx]*c.mass/1e3
                monitor_nucs_grams[i] += nuc_grams
            # monitor cells
            record_drop = False
            record_file = None
            if c.id in monitor_cells:
                record_drop = True
                record_file = os.path.join(
                    step_dir, f"c{c.id}_drop_ele.csv")
                with open(record_file, 'w') as fo:
                    fo.write("Nuclide,Atoms(atoms/kg)\n")
            total_dropped_atoms = mat.fispact2mcnp(ntrans_avail_nucs,
                                                   record_drop=record_drop,
                                                   record_file=record_file,
                                                   total_dropped_atoms=total_dropped_atoms)
            c.update_material(mat)
            current_mid += 1
        # record purified nuclides
        if nuc_treatment:
            purified_nucs_file = f"purified_nucs.csv"
            if current_step == 0:
                # init the purified nucs file
                cnt = 'Iteration step'
                for nuc in nucs_to_treat:
                    cnt = f"{cnt},{nuc}(atoms),{nuc}(grams)"
                with open(purified_nucs_file, 'w') as fo:
                    fo.write(f"{cnt}\n")
            # update the purified nucs file
            cnt = f'{current_step}'
            for i, nuc in enumerate(nucs_to_treat):
                cnt = f"{cnt},{format_single_output(purified_atoms[i])},{format_single_output(purified_grams[i])}"
            with open(purified_nucs_file, 'a') as fo:
                fo.write(f"{cnt}\n")
        # record total dropped atoms
        if monitor_cells:
            with open(record_file_total, 'a') as fo:
                fo.write(
                    f"{current_step},{format_single_output(total_dropped_atoms)}\n")
        # monitor nucs
        if monitor_nucs:
            cnt = f'{current_step}'
            for i, nuc in enumerate(monitor_nucs):
                cnt = f"{cnt},{format_single_output(monitor_nucs_atoms[i])},{format_single_output(monitor_nucs_grams[i])}"
            with open(monitor_nucs_file, 'a') as fo:
                fo.write(f"{cnt}\n")
        if current_step < total_steps - 1:
            # update mcnp input file
            next_step = current_step + 1
            step_dir = os.path.join(dump_dir, f"step{next_step}")
            ofname = os.path.join(step_dir, f"mcnp_input_step{next_step}")
            update_mcnp_input_materials(mcnp_input, cells_need_cal, ofname)
            tally_numbers = get_tally_numbers(mcnp_input)
            update_mcnp_input_tallies(
                ofname, cells_need_cal, tid_start=max(tally_numbers))
            # update status
            settings.update_mat_evo_status(
                status_file, total_steps, next_step, 'PRE')
            print(f"End of NATF {aim}, step {current_step}, {stat}")
        if current_step == total_steps - 1:
            # deal with the fispact output and data analysis
            # the finial post processing, perform CELL_ACT_POST
            aim = 'CELL_ACT_POST'
            # [radwaste] standard
            rwss = settings.get_radwaste_standards(config)
            # get the cooling times
            cooling_times = settings.get_cooling_times(irradiation_scenario)
            cooling_times_cul = settings.get_cooling_times_cul(cooling_times)

            # read the activation responses
            read_fispact_output_cell(cells_need_cal, work_dir, aim,
                                     cooling_times_cul, fispact_files_dir=fispact_files_dir)
            treat_nuc_responses(cells_need_cal, parts, nuc_treatment)
            cell_act_post_process(parts, step_dir, model_degree,
                                  aim, cooling_times_cul, rwss=rwss)
            # update status
            settings.update_mat_evo_status(
                status_file, total_steps, total_steps-1, 'FIN')
            print(
                f"End of NATF CELL_MAT_EVO and CELL_ACT_POST, step {current_step}, {stat}")
            print(f'NATF: CELL_MAT_EVO completed!\n')


def natf_run():
    # first check the configure file to get running information
    config_filename = "config.ini"
    config = configparser.ConfigParser()
    config.read(config_filename)
    settings.check_config(filename=config_filename)

    # general
    aim = config.get('general', 'aim')
    print(f'Starting NATF: {aim}')
    if aim == 'CELL_RWC_VIS':
        natf_cell_rwc_vis(config)
    if aim in ('CELL_ACT_PRE', 'CELL_DPA_PRE'):
        natf_cell_act_pre(config)
    if aim in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        natf_cell_act_post(config)
    if aim == 'COOLANT_ACT_PRE':
        natf_coolant_act_pre(config)
    if aim == 'COOLANT_ACT_POST':
        natf_coolant_act_post(config)
    if aim == 'CELL_MAT_EVO':
        natf_cell_mat_evo(config)
    return


# codes for test functions
if __name__ == '__main__':
    pass

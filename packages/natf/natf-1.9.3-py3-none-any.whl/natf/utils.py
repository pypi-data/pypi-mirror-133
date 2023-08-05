#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import with_statement, print_function
import math
import numpy as np
import os
import filecmp

thisdir = os.path.dirname(os.path.abspath(__file__))
# constant variables
avogad = 6.0220434469282E+23  # avogadro number (molecules/mole), from MCNP6
ELE_TABLE = ('H', 'He', 'Li', 'Be', 'B',
             'C', 'N', 'O', 'F', 'Ne',
             'Na', 'Mg', 'Al', 'Si', 'P',
             'S', 'Cl', 'Ar', 'K', 'Ca',
             'Sc', 'Ti', 'V', 'Cr', 'Mn',
             'Fe', 'Co', 'Ni', 'Cu', 'Zn',
             'Ga', 'Ge', 'As', 'Se', 'Br',
             'Kr', 'Rb', 'Sr', 'Y', 'Zr',
             'Nb', 'Mo', 'Tc', 'Ru', 'Rh',
             'Pd', 'Ag', 'Cd', 'In', 'Sn',
             'Sb', 'Te', 'I', 'Xe', 'Cs',
             'Ba', 'La', 'Ce', 'Pr', 'Nd',
             'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
             'Dy', 'Ho', 'Er', 'Tm', 'Yb',
             'Lu', 'Hf', 'Ta', 'W', 'Re',
             'Os', 'Ir', 'Pt', 'Au', 'Hg',
             'Tl', 'Pb', 'Bi', 'Po', 'At',
             'Rn', 'Fr', 'Ra', 'Ac', 'Th',
             'Pa', 'U', 'Np', 'Pu', 'Am',
             'Cm', 'Bk', 'Cf', 'Es', 'Fm')
E_GROUP_FILES = {69: "wims-69.txt",
                 175: "vitamin-j-175.txt",
                 315: "tripoli-315.txt",
                 709: "ccfe-709.txt",
                 1102: "ukaea-1102.txt"}


def get_e_group_filename(e_group_size):
    """
    Energy group structure files are stored under natf/data/energy_groups
    """
    if e_group_size not in E_GROUP_FILES.keys():
        raise ValueError(f"energy group {e_group_size} not supported!")
    filename = E_GROUP_FILES[e_group_size]
    filename = os.path.join(thisdir, "data", "energy_groups", f"{filename}")
    return filename


def get_e_group(e_group_size, unit='MeV', reverse=True, with_lowest_bin=True):
    """Read the energy group data.

    Parameters:
    -----------
    e_group_size : int
        The energy group size. Eg. 69/175/315/709/1102
    unit : str
        Output unit of the energy bin data
    reverse : bool
        If reverse is true, the output values are from high energy to low energy (FISPACT style).
        Else, output from low energy to high energy (MCNP style).

    Returns:
    --------
    values : np.ndarray
        The energy group in numpy array.
    """

    filename = get_e_group_filename(e_group_size)
    values = np.zeros(shape=(e_group_size+1, ), dtype=np.float)
    with open(filename, 'r') as fin:
        count = 0
        while True:
            line = fin.readline()
            if line == '':
                break
            value = float(line.strip())
            values[count] = value
            count += 1
            if count > e_group_size + 1:
                raise ValueError(
                    f"energy group file {filename} contains wrong data")
    if unit == 'MeV':
        values = np.divide(values, 1e6)
    if not with_lowest_bin:
        values = values[0:-1]
    if not reverse:
        values = values[::-1]
    return values


def get_ele_table():
    return ELE_TABLE


def log(func):
    def wrapper(*args, **kw):
        print('running {0}:'.format(func.__name__))
        return func(*args, **kw)
    return wrapper


def time_to_sec(value, unit):
    """time_to_sec convert the time of cooling time to the unit of sec.
    input parameters:value, a float number of time,
                     unit, a string of time unit, like SECS, MINS, HOURS, DAYS, YEARS
    return value: value, a float number of time in unit of sec"""
    # convert value to float incase of it's a string
    value = float(value)
    # unit check
    if unit.lower() not in ('s', 'sec', 'secs', 'second', 'seconds',
                            'm', 'min', 'mins', 'minute', 'minutes',
                            'h', 'hr', 'hour', 'hours',
                            'd', 'day', 'days',
                            'y', 'a', 'year', 'years'):
        raise ValueError('unit of time must in given value, not arbitrary one')
    if unit.lower() in ('s', 'sec', 'secs', 'second', 'seconds'):
        return value * 1.0
    if unit.lower() in ('m', 'min', 'mins', 'minute', 'minutes'):
        return value * 60.0
    if unit.lower() in ('h', 'hr', 'hour', 'hours'):
        return value * 3600.0
    if unit.lower() in ('d', 'day', 'days'):
        return value * 3600 * 24.0
    if unit.lower() in ('y', 'a', 'year', 'years'):
        return value * 3600 * 24 * 365.25


def time_sec_to_unit(value, unit):
    """
    Convert time from unit (s) to another unit.
    """
    value = float(value)
    # unit check
    if unit.lower() not in ('s', 'sec', 'secs', 'second', 'seconds',
                            'm', 'min', 'mins', 'minute', 'minutes',
                            'h', 'hr', 'hour', 'hours',
                            'd', 'day', 'days',
                            'y', 'a', 'year', 'years'):
        raise ValueError('unit of time must in given value, not arbitrary one')
    if unit.lower() in ('s', 'sec', 'secs', 'second', 'seconds'):
        return value / 1.0
    if unit.lower() in ('m', 'min', 'mins', 'minute', 'minutes'):
        return value / 60.0
    if unit.lower() in ('h', 'hr', 'hour', 'hours'):
        return value / 3600.0
    if unit.lower() in ('d', 'day', 'days'):
        return value / (3600 * 24.0)
    if unit.lower() in ('y', 'a', 'year', 'years'):
        return value / (3600 * 24 * 365.25)


def proper_time_unit(value):
    """Convert the time to more human readable time unit.
    Parameters:
    -----------
    value : float
        The time in unit of [s]

    Returns:
    --------
    value : float
        The time in proper unit
    unit : str
        The output time unit, could be [s], [h], [d] or [y]
    """
    if value < 3600:
        return value, 's'
    # try hour
    unit = 'h'
    val = time_sec_to_unit(value, unit)
    if val < 24.0:
        return val, unit
    # try day
    unit = 'd'
    val = time_sec_to_unit(value, unit)
    if val < 365.25:
        return val, unit
    # use year
    unit = 'y'
    val = time_sec_to_unit(value, unit)
    return val, unit


def sgn(value):
    """sgn return 1 for number greater than 0.0, return -1 for number smaller than 0"""
    if not isinstance(value, (int, float)):
        raise ValueError('value for sgn must a number of int or float')
    if value == 0:
        sgn = 0
    if value < 0.0:
        sgn = -1
    if value > 0.0:
        sgn = 1
    return sgn


def ci2bq(value):
    """Convert unit from Ci to Bq."""
    # input check
    if not isinstance(value, float):
        raise ValueError("Input value for Ci must be float")
    if value < 0:
        raise ValueError("Negative input for Ci")
    return value * 3.7e+10


def scale_list(value):
    """scale_list: scale a list of float, normalized to 1"""
    # check the input
    if not isinstance(value, list):
        raise ValueError('scale_list can only apply to a list')
    for item in value:
        if not isinstance(item, float):
            raise ValueError('scale_list can only apply to a list of float')
    # scale the list
    t = sum(value)
    for i in range(len(value)):
        value[i] /= t
    return value


def get_ct_index(ct, cts):
    """
    Get the index of a cooling time in cooling_times. As there is roundoff
    error in data.

    Parameters:
    -----------
    ct: float
        The cooling time to find.
    cts: list of float
        The cooling times.
    """
    for i in range(len(cts)):
        if math.isclose(ct, cts[i], rel_tol=1e-2):
            return i
    raise ValueError("ct {0} not found".format(ct))


def is_short_live(half_life, threshold=30):
    """
    Check whether the nuclide is short life (half life <= 30 years) nuclide.
    """
    # input check
    try:
        half_life = float(half_life)
    except:
        raise ValueError("half_life must be a float")
    if half_life < 0:
        raise ValueError("half_life < 0, invalide")
    # 30 year
    threshold_s = 60.0 * 60 * 24 * 365.25 * threshold
    if half_life <= threshold_s:
        return True
    else:
        return False


def data_to_line_1d(key, value, delimiter=',', postfix='\n', decimals=5):
    """
    Create a print line for given key and value.
    """
    data_content = ''
    if isinstance(value, list) or isinstance(value, np.ndarray):
        for i, item in enumerate(value):
            if i == 0:
                data_content = format_single_output(item, decimals=decimals)
            else:
                data_content = delimiter.join(
                    [data_content, format_single_output(item, decimals=decimals)])
    else:
        data_content = format_single_output(value, decimals=decimals)

    if key is not None:
        line = delimiter.join([format_single_output(
            key, decimals=decimals), data_content])
    else:
        line = data_content
    return line+postfix


def format_single_output(value, decimals=5):
    """
    Format a single item for output.
    """
    if isinstance(value, float):
        if decimals is None:
            return str(value)
        else:
            style = "{0:."+str(decimals)+"E}"
            return style.format(value)
    else:
        return str(value)


def str2float(s):
    """
    Convert string to float. Including some strange value.
    """
    try:
        value = float(s)
        return value
    except:
        if '-' in s:
            base = s.split('-')[0]
            index = s.split('-')[1]
            s_fix = ''.join([base, 'E-', index])
            return float(s_fix)
        else:
            raise ValueError("{0} can't convert to float".format(s))


def calc_ctr_flag_chn2018(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Eg: rwc='Clearance', rwcs=['HLW', 'ILW'], flag is '>'.
    Eg: rwc='ILW', rwcs=['LLW', 'VLLW'], flag is '<'.
    """
    class_dict = {'Clearance': 0, 'VLLW': 1, 'LLW': 2, 'ILW': 3, 'HLW': 4}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'


def calc_ctr_flag_usnrc(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Supported standard: 'USNRC' and 'USNRC_FETTER'.
    Eg: rwc='LLWA', rwcs=['LLWC', 'LLWB'], flag is '>'.
    Eg: rwc='ILW', rwcs=['LLWC', 'LLWB'], flag is '<'.
    """
    class_dict = {'LLWA': 0, 'LLWB': 1, 'LLWC': 2, 'ILW': 3}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'


def calc_ctr_flag_uk(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Eg: rwc='LLW', rwcs=['HLW', 'ILW'], flag is '>'.
    Eg: rwc='HLW', rwcs=['ILW', 'LLW'], flag is '<'.
    """
    class_dict = {'LLW': 0, 'ILW': 1, 'HLW': 2}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'


def calc_ctr_flag_russian(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Eg: rwc='Clearance', rwcs=['HLW', 'ILW'], flag is '>'.
    Eg: rwc='ILW', rwcs=['LLW', 'VLLW'], flag is '<'.
    """
    class_dict = {'LLW': 0, 'ILW': 1, 'HLW': 2}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'


def calc_ctr(cooling_times, rwcs, classes, standard='CHN2018', out_unit='a', decimals=2):
    """
    Calculate cooling time requirement for specific rwc.

    Parameters:
        cooling_times: list or pandas DataFrame series
            Cooling times, unit: s.
        rwcs: list
            Radwaste classes for each cooling time.
        classes: list
            Radwaste types.
            Eg: for CHN2018: ['HLW', 'ILW', 'LLW', 'VLLW', 'Clearance']
        standard: string
            Radwaste standard used. Supported standards: 'CHN2018', 'USNRC', 'UK'.
        out_unit: string
            Unit of output unit of cooling time. Supported value: 's', 'a'.

    Returns:
        ctr: list of strings
            Required cooling times (in string).
    """
    cooling_times = list(cooling_times)
    if out_unit == 'a':
        # unit conversion
        for i, ct in enumerate(cooling_times):
            cooling_times[i] = time_sec_to_unit(ct, 'a')

    exist_rwcs = list(set(rwcs))
    # find rwc in rwcs
    ctr = []
    for i, item in enumerate(classes):
        if standard in ['USNRC', 'USNRC_FETTER'] and item == 'LLW':
            item = 'LLWC'
        if item in rwcs:
            index = rwcs.index(item)
            ctr.append(format_single_output(
                cooling_times[index], decimals=decimals))
        else:
            if standard == 'CHN2018':
                flag = calc_ctr_flag_chn2018(item, exist_rwcs)
            elif standard in ['USNRC', 'USNRC_FETTER']:
                flag = calc_ctr_flag_usnrc(item, exist_rwcs)
            elif standard == 'UK':
                flag = calc_ctr_flag_uk(item, exist_rwcs)
            elif standard == 'RUSSIAN':
                flag = calc_ctr_flag_russian(item, exist_rwcs)
            else:
                raise ValueError(f"standard: {standard} not supported")

            if flag == '>':
                ctr.append(''.join([flag, format_single_output(
                    cooling_times[-1], decimals=decimals)]))
            else:
                ctr.append(''.join([flag, format_single_output(
                    cooling_times[0], decimals=decimals)]))
    return ctr


def calc_recycle_ctr(cooling_times, cds, rh='CRH', out_unit='a', decimals=2):
    """
    Calculate cooling time requirement for recycling.

    Parameters:
        cooling_times: list or pandas DataFrame series
            Cooling times, unit: s.
        cds: list
            Contact dose rate for each cooling time.
        classes: list
            Recycling methods.
            Could be CRH and ARH. [CRH, ARH]
        out_unit: string
            Unit of output unit of cooling time. Supported value: 's', 'a'.

    Returns:
        ctr: float
           In unit of out_unit.
    """
    cooling_times = list(cooling_times)
    if out_unit == 'a':
        # unit conversion
        for i, ct in enumerate(cooling_times):
            cooling_times[i] = time_sec_to_unit(ct, 'a')
    # determin limit
    if rh.upper() == 'CRH':
        limit = 1e-2
    elif rh.upper() == 'ARH':
        limit = 1e4
    else:
        raise ValueError(f"rh {rh} not supported, use 'CRH' or 'ARH'")
    # calc ctr
    for i, ct in enumerate(cooling_times):
        if i == 0 and cds[0] < limit:
            ctr = ''.join(['<', format_single_output(
                cooling_times[0], decimals=decimals)])
            return ctr
        if cds[i-1] > limit and cds[i] <= limit:
            ctr = ''.join([format_single_output(
                cooling_times[i], decimals=decimals)])
            return ctr
    # cds do not meet limit
    ctr = ''.join(['>', format_single_output(
        cooling_times[-1], decimals=decimals)])
    return ctr


def mcnp_style_str_append(s, value, indent_length=6):
    """append lines as mcnp style, line length <= 80"""
    indent_str = ' '*indent_length
    s_tmp = ''.join([s, ' ', format_single_output(value, decimals=None)])
    if len(s_tmp.split('\n')[-1]) >= 80:
        s_tmp = ''.join([s, '\n', indent_str, ' ',
                        format_single_output(value, decimals=None)])
    s = s_tmp
    return s


def is_blank_line(line):
    """check blank line"""
    line_ele = line.split()
    if len(line_ele) == 0:
        return True
    else:
        return False


def scale_list(value):
    """scale_list: scale a list of float, normalized to 1"""
    # check the input
    if not isinstance(value, list):
        raise ValueError('scale_list can only apply to a list')
    for i, item in enumerate(value):
        try:
            value[i] = float(item)
        except:
            raise ValueError('scale_list can only apply to a list of float')
    # scale the list
    t = sum(value)
    for i in range(len(value)):
        value[i] /= t
    return value


def diff_check_file(f1, f2):
    command = ''.join(["diff ", "--strip-trailing-cr ", f1, " ", f2])
    flag = os.system(command)
    return flag


def compare_lists(l1, l2):
    """
    Compare two lists.
    """
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True


def str_to_unicode(s):
    """
    This function convert a str from binary or unicode to str (unicode).
    If it is a list of string, convert every element of the list.

    Parameters:
    -----------
    s : str or list of str

    Returns:
    --------
    s : text str or list of unicode str
    """
    if isinstance(s, str) or isinstance(s, bytes):
        # it is a str, convert to text str
        try:
            s = s.decode('utf-8')
        except:
            pass
        return s
    else:
        for i, item in enumerate(s):
            try:
                s[i] = item.decode('utf-8')
            except:
                pass
        return s


def is_float(s):
    """
    This function checks whether a string can be converted as a float number.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def str_almost_same(s1, s2, rel_tol=1e-9):
    """
    This function is used to compare two string to check whether they are
    almost the same.
    Return True if two strings are exactly the same.
    Return True if two strings are almost the same with only slight difference
    of float decimals.
    Return False if two strings are different.
    """
    # if string can be converted to float number
    if is_float(s1) and is_float(s2):
        return math.isclose(float(s1), float(s2), rel_tol=rel_tol)
    else:
        # not a number
        return s1 == s2


def line_almost_same(l1, l2, rel_tol=1e-9):
    """
    This function is used to compare two lines (read from files). If they are
    the same, or almost the same (with only slight difference on float
    numbers), return True. Otherwise, return False.

    Parameters:
    -----------
    l1 : str
        Line 1
    l2 : str
        Line 2
    rel_tol : float
        Relative tolerance for float comparison

    Returns:
    --------
    True, if two lines are the same. False, if they are different.
    """
    if l1 == l2:
        # exactly the same
        return True
    else:
        # There are differences
        tokens1 = l1.strip().split()
        tokens2 = l2.strip().split()
        if len(tokens1) != len(tokens2):
            return False
        else:
            # compare string elements of the line
            for i in range(len(tokens1)):
                if str_almost_same(tokens1[i], tokens2[i], rel_tol=rel_tol):
                    pass
                else:
                    return False
        return True


def file_almost_same(f1, f2, rel_tol=1e-9):
    """
    For some reasons, it's useful to compare two files that are almost the
    same. Two files, f1 and f2, the text contents are exactly the same, but
    there is a small difference in numbers. Such as the difference between
    'some text 9.5' and 'some text 9.500000000001'.
    For example, in PyNE test files, there are some expected file generated
    by python2, however, the the file generated by python3 may have difference
    in decimals.

    Parameters:
    -----------
    f1 : str 
        Filename of file 1 or lines
    f2 : str
        Filename of file 2 or lines
    rel_tol : float
        Relative tolerance for float numbers

    Returns:
    True : bool
        If two file are exactly the same, or almost the same with only decimal
        differences.
    False : bool
        If the strings of the two files are different and/or their numbers
        differences are greater than the tolerance
    """
    if os.path.isfile(f1) and os.path.isfile(f2):
        if filecmp.cmp(f1, f2):
            # precheck
            return True
    else:
        # read lines of f1 and f2, convert to unicode
        if os.path.isfile(f1):
            with open(f1, 'r') as f:
                lines1 = f.readlines()
        else:
            lines1 = f1
        lines1 = str_to_unicode(f1)
        lines1 = lines1.strip().split(u'\n')

        if os.path.isfile(f2):
            with open(f2, 'r') as f:
                lines2 = f.readlines()
        else:
            lines2 = f2
        lines2 = str_to_unicode(f2)
        lines2 = lines2.strip().split(u'\n')

        # compare two files
        # check length of lines
        if len(lines1) != len(lines2):
            return False
        # check content line by line
        for i in range(len(lines1)):
            if line_almost_same(lines1[i], lines2[i], rel_tol=rel_tol):
                pass
            else:
                return False

    # no difference found
    return True


def neutron_intensity_to_power(value):
    """
    Convert the neutron intensity to fusion power [MW].
    1 MW fusion power is equivalent to 3.545e+17 n/s
    """
    return value / 3.545e17


# codes for test functions
if __name__ == '__main__':
    pass

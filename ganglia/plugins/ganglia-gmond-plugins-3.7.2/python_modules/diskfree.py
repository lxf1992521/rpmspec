#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Disk Free gmond module for Ganglia
#
# This module reads a list of mountpoints from the "mounts" parameter (probably
# /proc/mounts) and creates a "disk_free_(absolute|percent)_*" metric for each
# mountpoint it finds.

import re
import os


# metric setting
MOUNTS_FILE = '/proc/mounts'
PARAMS = {
    'metric_prefix': 'disk_free_',
    'min_disk_size': 1,
    'explicit_mounts_fs': ['ext2', 'ext3', 'ext4', 'xfs'],
    'exclude_mounts_point': [],
    'explicit_mounts_point': [],
}
MODES = {
    'absolute': 'GB',
    'percent': '%',
}
PATHS = []


# define get Value Function
def get_value(name):
    """Return a value for the requested metric"""

    # parse unit type and path from name
    name_parser = re.match("^%s(absolute|percent)_(.*)$" % PARAMS['metric_prefix'], name)
    unit_type = name_parser.group(1)
    if name_parser.group(2) == 'rootfs':
        path = '/'
    else:
        path = '/' + name_parser.group(2).replace('_', '/')

    # get fs stats
    try:
        disk = os.statvfs(path)
        if unit_type == 'percent':
            result = (float(disk.f_bavail) / float(disk.f_blocks)) * 100
        else:
            result = (disk.f_bavail * disk.f_frsize) / float(2**30)  # GB
    except OSError:
        result = 0
    except ZeroDivisionError:
        result = 0

    return result


def metric_init(lparams):
    """Initialize metric descriptors"""

    global PARAMS, PATHS

    # set parameters and PATHS
    for key in lparams:
        if key == "exclude_mounts_point" or key == "explicit_mounts_point" or key == "explicit_mounts_fs":
            PARAMS[key] = lparams[key].split()
        else:
            PARAMS[key] = lparams[key]

    try:
        f = open(MOUNTS_FILE)
    except IOError:
        f = []

    # fix chroot bugs
    dir_tmp = {}
    for path in f:
        path = path.split()
        if path[1] in PARAMS['exclude_mounts_point']:
            continue
        elif path[1] in PARAMS['explicit_mounts_point'] or path[2] in PARAMS['explicit_mounts_fs']:
            if dir_tmp.get(path[0], False):
                if len(dir_tmp[path[0]]) > len(path[1]):
                    dir_tmp[path[0]] = path[1]
            else:
                dir_tmp[path[0]] = path[1]

    PATHS = list(set(dir_tmp.values()))

    # parse mounts and create descriptors
    descriptors = []

    for line in PATHS:

        if line == '/':
            path_key = 'rootfs'
        else:
            path_key = line[1:].replace('/', '_')

        # Calculate the size of the disk. We'll use it exclude small disks
        disk = os.statvfs(line)
        disk_size = (disk.f_blocks * disk.f_frsize) / float(2**30)

        if disk_size >= float(PARAMS['min_disk_size']):
            for unit_type in MODES:
                descriptors.append({
                    'name': PARAMS['metric_prefix'] + unit_type + '_' + path_key,
                    'call_back': get_value,
                    'time_max': 60,
                    'value_type': 'float',
                    'units': MODES[unit_type],
                    'slope': 'both',
                    'format': '%f',
                    'description': "Disk space available (%s) on %s" % (MODES[unit_type], line),
                    'groups': 'disk'
                    })

    return descriptors


def metric_cleanup():
    """Cleanup"""

    pass


# the following code is for debugging and testing
if __name__ == '__main__':

    lparamss = {
        'exclude_mounts_point': "/boot /mnt",
        'explicit_mounts_point': "/dev/shm"
    }

    descriptors = metric_init(lparamss)
    for d in descriptors:
        print (('%s = %s') % (d['name'], d['format'])) % (d['call_back'](d['name']))

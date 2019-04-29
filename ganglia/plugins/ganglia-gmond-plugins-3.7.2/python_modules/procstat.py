#!/usr/bin/python

import re
import time

METRICS = {
    'proc_created': {
        'fname': 'processes',
        'value_type': 'float',
        'units': 'per second',
        'slope': ['counter', time.time(), 0 ],
        'value': 0,
        'format': '%f',
        'description': 'number of created process per second'
    },
    'proc_blocked': {
        'fname': 'procs_blocked',
        'value_type': 'uint',
        'slope': ['both'],
        'value': 0,
        'format': '%d',
        'description': 'number of blocked process'
    }
}

descriptors = []

# ====================================
def get_value(mname):

    try:
        file = open('/proc/stat', 'r')
        now_time = time.time()
    except IOError:
        return 0

    metrics = {}
    for line in file:
        parts = re.split("\s+", line)
        metrics[parts[0]] = float(parts[1])

    if METRICS[mname]['slope'][0] == 'counter':
        METRICS[mname]['value'] = (metrics[METRICS[mname]['fname']] - METRICS[mname]['slope'][2])/(now_time - METRICS[mname]['slope'][1])
        METRICS[mname]['slope'][1] = now_time
        if METRICS[mname]['slope'][2] == 0:
            METRICS[mname]['value'] = 0.0
        METRICS[mname]['slope'][2] = metrics[METRICS[mname]['fname']]
    else:
        METRICS[mname]['value'] = metrics[METRICS[mname]['fname']]

    return METRICS[mname]['value']

def metric_init(params):

    global descriptors, METRICS

    for line in METRICS:
        descriptors.append({
            'name': line,
            'call_back': get_value,
            'time_max': 60,
            'value_type': METRICS[line].get('value_type', 'string'),
            'units': METRICS[line].get('units', ''),
            'slope': METRICS[line]['slope'][0],
            'format': METRICS[line].get('format', '%s'),
            'description': METRICS[line].get('description', ''),
            'groups': METRICS[line].get('groups', 'process'),
        })

    return descriptors


def metric_cleanup():
    '''Clean up the metric module.'''
    pass


#This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        print d['name']
        print d['call_back'](d['name'])
        # print '%s = ' + d['format'] % (d['name'],  d['call_back'](d['name']))

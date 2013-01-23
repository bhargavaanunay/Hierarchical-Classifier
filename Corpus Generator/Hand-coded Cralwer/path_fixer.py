'''
Created on Jan 17, 2013

@author: ayush
'''

import os
import sys

def fix_path(path):
    offset = 0
    if path[-1] != '/':
        path = path + '/'
    if path[0] == '/':
        offset = 1
    idx = path.find('/', offset)
    while idx != -1:
        try:
            if not os.path.exists(path[:idx]):
                os.makedirs(path)
            idx = path.find('/', idx + 1)
        except:
            sys.exit("Unable to create path: " + path[:idx + 1])
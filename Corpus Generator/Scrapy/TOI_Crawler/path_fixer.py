'''
Created on Jan 17, 2013

@author: ayush
'''

import os

def fix_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
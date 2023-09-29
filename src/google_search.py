#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Filename : google_search.py
@CreatedTime : 2023/09/26 16:17


This program has a function to find the as much as possible VMs in Vulnhub that can be attacked using Metasploit.

'''


############################################################################
# Import modules
############################################################################

############################################################################

__author__ = 'masjohncook'
__copyright__ = '(C)Copyright 2023'
__credits__ = []
__license__ = 'None'
__version__ = '0.0.1'
__maintainer__ = 'masjohncook'
__email__ = 'mas.john.cook@gmail.com'
__status__ = 'None'

############################################################################



# Load VM names
with open('vm_names.json', 'r') as f:
    vms = json.load(f)


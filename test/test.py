#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Filename : test.py
@CreatedTime : 2023/10/11 17:21


This program has a function to test the Google search module

'''


############################################################################
# Import modules
############################################################################
from googlesearch import search


qry = "google scholar"
num_of_results = 5


for results in search(qry, num_results=num_of_results):
    print(results)
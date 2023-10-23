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
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.text('metasploit', region='wt-wt', safesearch='off', timelimit='y', max_results=3):
        print(r['href'])
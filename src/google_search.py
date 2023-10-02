#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Filename : google_search.py
@CreatedTime : 2023/09/26 16:17


This program has a function to find the as much as possible VMs in Vulnhub that can be attacked using Metasploit.

'''


############################################################################
# Import modules
###########################################################################
from googlesearch import search
import argparse
import json
import time
from bs4 import BeautifulSoup
import requests
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

class GSearch():
    def __init__(self):
        pass
    
    def loadLinks(self, json_file):
        try:
            with open(json_file, 'r') as f:
                vms = json.load(f)
            return vms
        except FileNotFoundError:
            print(f"Error: {json_file} not found.")
            return {'link_list':[]}
        except json.JSONDecodeError:
            print(f"Error: {json_file} is not valid JSON file")
            return {'link_list':[]}
    
    def searching(self, query):
        wl_list = []
        num_of_results = 5
        qry = "walkthrough {}".format(query)
        while True:
            try:
                for results in search(qry, num_results=num_of_results):
                    wl_list.append(results)
                break
            except Exception as e:
                error_message = str(e)
                if "429 Client Error: Too Many Requests" in error_message:
                    print("Too many request, sleep for 10 minutes")
                    time.sleep(600)
                else:
                    print(f"Error occurred while searching: {e}")
                    break
        return wl_list
        
    def checkForTerm(self, url, term="metasploit"):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        
        for paragraph in paragraphs:
            if term.lower() in paragraph.get_text().lower():
                return True
        return False
    
    def saveToJsonMetasploit(self, data, filename='result_metasploit.json'):
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    def saveToJsonNonMetasploit(self, data, filename='result_non_metasploit.json'):
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    
    def main(self, input_file):
        vm_list = self.loadLinks(input_file).get('link_list', [])
        no = 1
        for vms in vm_list:
            if vms:
                print("{}. {}".format(no, vms[0]))
                list_wl_link = self.searching(vms[0])
                no += 1
                time.sleep(20)
                for link in list_wl_link:
                    print(link)
                    if self.checkForTerm(link):
                        print(f"The term 'metasploit' was found at {link}")
                        self.saveToJsonMetasploit({'vm': vms[0], 'link': link})
                        break
                    else:
                        print(f"The term 'metasploit' was not found at {link}")
                        self.saveToJsonNonMetasploit({'vm': vms[0], 'link': link})



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Google and check the link fot metasploit related info")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the JSON input file')
    args = parser.parse_args()
    
    gs = GSearch()
    gs.main(args.input_file)
    
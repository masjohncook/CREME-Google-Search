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
from duckduckgo_search import DDGS
import argparse
import json
import time
from bs4 import BeautifulSoup
import requests
import logging
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
        self.setupLogging()
        self.logger = logging.getLogger(self.__class__.__name__) 
    
    def setupLogging(self):
        logging.basicConfig(filename='search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def loadLinks(self, json_file):
        try:
            with open(json_file, 'r') as f:
                vms = json.load(f)
            return vms
        except FileNotFoundError:
            self.logger.info(f"Error: {json_file} not found.")
            return {'link_list':[]}
        except json.JSONDecodeError:
            self.logger.info(f"Error: {json_file} is not valid JSON file")
            return {'link_list':[]}
    
    def searching(self, query):
        wl_list = []
        num_of_results = 3
        qry = "walkthrough and {}".format(query)
        success = False
        while not success:
            try:
                print(f"Searching {qry}")
                self.logger.info(f"Searching {qry}")
                with DDGS() as ddgs:
                    for results in ddgs.text(qry, 
                                            region='wt-wt', 
                                            safesearch='off', timelimit='y', max_results=num_of_results):
                        print(results['href'])
                        self.logger.info(results['href'])
                        wl_list.append(results['href'])
                success = True
            except Exception as e:
                error_message = str(e)
                if "429 Client Error: Too Many Requests" in error_message:
                    print("Too many request, sleep for 120 minutes")
                    self.logger.info("Too many request, sleep for 120 minutes")
                    time.sleep(7200)
                else:
                    self.logger.info(f"Error occurred while searching: {e}")
                    break
        return wl_list
        
    def checkForMetasploit(self, url, term="metasploit"):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.info(f"Error accessing {url}: {e}")
            return False
        print("Checking for term 'metasploit' at {}".format(url))
        self.logger.info("Checking for term 'metasploit' at {}".format(url))
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        
        for paragraph in paragraphs:
            if term.lower() in paragraph.get_text().lower():
                return True
        return False
    
    def checkForExploit(self, url, term="exploit"):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.info(f"Error accessing {url}: {e}")
            return False
        print("Checking for term 'exploit' at {}".format(url))
        self.logger.info("Checking for term 'exploit' at {}".format(url))
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        
        for paragraph in paragraphs:
            if term.lower() in paragraph.get_text().lower():
                return True
        return False
    
    def saveToJsonMetasploit(self, data, filename='result_metasploit.json'):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
            
        existing_data.append(data)
        
        with open(filename, 'w') as f:
            json.dump(existing_data, f)
            
    def saveToJsonExploit(self, data, filename='result_exploit.json'):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
            
        existing_data.append(data)
        
        with open(filename, 'w') as f:
            json.dump(existing_data, f)
    
    def saveToJsonMExploit(self, data, filename='result_non_mexploit.json'):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
            
        existing_data.append(data)
        
        with open(filename, 'w') as f:
            json.dump(existing_data, f)
    
    def main(self, input_file):
        vm_list = self.loadLinks(input_file).get('link_list', [])
        no = 1
        max_results = 100
        total_entries = len(vm_list)
        
        for i in range(0, total_entries, max_results):
            sublist = vm_list[i:i+max_results]
            
            for vms in sublist:
                if vms:
                    print("{}. {}".format(no, vms[0]))
                    list_wl_link = self.searching(vms[0])
                    no += 1
                    time.sleep(30)
                    for link in list_wl_link:
                        print(link)
                        if self.checkForMetasploit(link):
                            print(f"The term 'metasploit' was found at {link}")
                            self.logger.info(f"The term 'metasploit' was found at {link}")
                            self.saveToJsonMetasploit({'vm': vms[0], 'link': link})
                            break
                        elif self.checkForExploit(link):
                            print(f"The term 'exploit' was found at {link}")
                            self.logger.info(f"The term 'exploit' was found at {link}")
                            self.saveToJsonExploit({'vm': vms[0], 'link': link})
                            break
                        else:
                            print(f"The term 'metasploit' was not found at {link}")
                            self.logger.info(f"The term 'metasploit' was not found at {link}")
                            self.saveToJsonMExploit({'vm': vms[0], 'link': link})
                    if no % max_results == 0 and  no != total_entries:
                        print(f"Reached {max_results} searches, waiting for 120 minutes...")
                        time.sleep(7200)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search on DuckDuckGo and check the link fot metasploit related info")
    parser.add_argument('-i', '--input_file', type=str, help='Path to the JSON input file')
    args = parser.parse_args()
    
    gs = GSearch()
    gs.main(args.input_file)
    
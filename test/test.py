import json

with open('all_link_lists.json', 'r') as f:
    vms = json.load(f)
    
    print(vms['link_list'][0][0])
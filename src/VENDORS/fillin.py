# powwu's done all the US work

import requests
import re
import json
import os
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse

table_header = "| Vendor | Switches | Lube | Stabs | Cables | Keycaps | Keyboards | Location |\n"
table_separa = "| - | - | - | - | - | - | - | - |\n"
table_line_template = "| {}  | - | - | - | - | - | - | {} |\n"

PATTERN = '<span.*>(.*)</span'
FILE_NAME = 'scraped_mechmap.json'

dict_of_sites = {}

if not os.path.isfile(FILE_NAME):
    # generate base file
    print("generating")
    content = requests.get('https://mechmap.tech').content
    for link in BeautifulSoup(content, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            try:
                link_name = str(link.contents[0])
                if 'span' in link_name:
                    link_name = re.search(PATTERN, link_name).group(1)
                link_details = urlparse(link['href'])
                za_link = f"{link_details.scheme}://{link_details.hostname}/"
                dict_of_sites[za_link] = {'link_name': link_name}
            except Exception:
                pass
    # serialize
    json_object = json.dumps(dict_of_sites, indent=4, sort_keys=True)
    with open(FILE_NAME, 'w') as json_dumper:
        json_dumper.write(json_object)
else:
    # load in pre-existing file
    with open(FILE_NAME, 'r') as json_file:
        dict_of_sites = json.load(json_file)
    print("found file!")

for site in dict_of_sites:
    # see if progress was saved
    if not dict_of_sites[site].get('region'):
        while True:
            region_interpret_string = input(f"Region for {dict_of_sites[site]['link_name']}: [1] NA [2] EU [3] AS+OC: ")
            try:
                region_interpret = int(region_interpret_string)
                if region_interpret == 1:
                    dict_of_sites[site]['region'] = 'NA'
                    break
                elif region_interpret == 2:
                    dict_of_sites[site]['region'] = 'EU'
                    break
                elif region_interpret == 3:
                    dict_of_sites[site]['region'] = 'AS+OC'
                    break
            except Exception:
                print("retrying...")
    if not dict_of_sites[site].get('local'):
        if dict_of_sites[site]['region'] != 'NA':
            local_string = input(f"Local region for {dict_of_sites[site]['link_name']}: ")
            if local_string:
                dict_of_sites[site]['local'] = local_string
    # save progress
    json_object = json.dumps(dict_of_sites, indent=4, sort_keys=True)
    with open(FILE_NAME, 'w') as json_dumper:
        json_dumper.write(json_object)


with open('VENDOR_EU.md', 'w') as eu_vendor_file:
    with open('VENDOR_ASOC.md', 'w') as asoc_vendor_file:
        eu_vendor_file.write(table_header)
        asoc_vendor_file.write(table_header)
        eu_vendor_file.write(table_separa)
        asoc_vendor_file.write(table_separa)
        for site_url, site_data in dict_of_sites.items():
            if site_data['region'] == 'AS+OC':
                asoc_vendor_file.write(table_line_template.format(f"[{site_data['link_name']}]({site_url})", site_data['local']))
            if site_data['region'] == 'EU':
                eu_vendor_file.write(table_line_template.format(f"[{site_data['link_name']}]({site_url})", site_data['local']))
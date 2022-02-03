#!/bin/python3
# usage: ./detect.py [site URL]
# pulls down site at URL given and reads it for any mention of keycaps, lube, stabs, etc.
# too lazy to do argument parsing

import requests
import sys


def search_for_mention(site_content: str, keyword: str):
    if keyword in site_content:
        print(f'{keyword} found')


site = sys.argv[1]
site_content = requests.get(site).text.lower()

search_for_mention(site_content, 'switch')
search_for_mention(site_content, 'lub')
search_for_mention(site_content, 'grease')
search_for_mention(site_content, 'stab')
search_for_mention(site_content, 'cable')
search_for_mention(site_content, 'keycap')
search_for_mention(site_content, 'keyboards')
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re
import json 
import cfscrape

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    
default_domain = "https://www.imdb.com"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

base_url = "https://www.imdb.com/find/?q=Kalki&ref_=nv_sr_sm"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
session = requests.Session()


cookies = {
    'user_id': '3316641453',
    'sku': '01J28X81T07BA9D023VY5JQRJAD_gamechanger_cue_piece'
}

initial_response = requests.get(base_url, headers=initial_headers)
response_text = initial_response.text
print(response_text)
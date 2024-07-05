import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
from urllib.parse import urlparse
import json

default_domain = "https://febbox.com/"
initial_headers = {
    'Referer': default_domain,
    'Accept-Language': 'de-DE',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"',
}

response_data = {
    'status': None,
    'status_code': None,
    'error': None,
    'headers': {},
    'streaming_urls': {},
    'downloading_urls': {}
}

qualities = ['1080p', '720p', '480p', '360p']

def extract_last_path(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    last_path_segment = path_segments[-1] if path_segments[-1] else path_segments[-2]
    return last_path_segment


def real_extract(url):
    file_path = extract_last_path(url)
    share_key = file_path
    base_url = f'{default_domain}share/{share_key}'
    
    initial_response = requests.get(base_url).text
    soup = BeautifulSoup(initial_response, "html.parser")
    file_id = soup.find("div", attrs={"class":"file"})['data-id']
    
    payload = {
        "fid" : file_id,
        "share_key": share_key, 
    }
    initial_response = requests.post("https://www.febbox.com/file/player", data=payload).text
    pattern = r'var\s+sources\s*=\s*(\[.*?\]);'
    match = re.search(pattern, initial_response)
    json_response = json.loads(match.group(1))
    unique_qualities = {}
    valid_qualities = ['1080P', '720P', '360P']
    filtered_files = {}
    pattern = re.compile(r'https://fr1-as01-1\.shegu\.net/')
    
    for source in json_response:
        quality = source['label']
        file_url = source.get('file')
        modified_url = file_url.replace("https://fr1-as01-1", "https://in1-as2-01")
        if quality in valid_qualities:
            if modified_url:
                filtered_files[quality.lower()] = modified_url


    response_data['streaming_urls'] = filtered_files
    response_data['downloading_urls'] = filtered_files
    return response_data
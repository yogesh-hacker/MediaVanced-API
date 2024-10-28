import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
from urllib.parse import urlparse
import json

default_domain = "https://febbox.com/"
initial_headers = {
    'Referer': 'https://www.febbox.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'text/plain, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

proxies = {
    "http": "http://gxyjptfg:7dwwrl2bkr9w@198.23.239.134:6540",
    "https": "http://gxyjptfg:7dwwrl2bkr9w@198.23.239.134:6540"
}

cookies = {
    'ui': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MjAzNTgxMjQsIm5iZiI6MTcyMDM1ODEyNCwiZXhwIjoxNzUxNDYyMTQ0LCJkYXRhIjp7InVpZCI6NDU0MDA0LCJ0b2tlbiI6IjdjNmMwMzEzYThhOGUzOTczNGZjMDI2MDQ2Y2JlNzkzIn19.LXWUfS004XLU6irNvIiNbxmG0weQ-mjZr7rzUhQdBjk'
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
    session = requests.Session()
    initial_response = session.get(base_url).text
    soup = BeautifulSoup(initial_response, "html.parser")
    
    file_id = None
    
    file_id_tag = soup.find("div", attrs={"class": "file"})
    if file_id_tag:
        file_id = file_id_tag.get('data-id')
    if not file_id:
        file_id_tag = soup.find("button", attrs={"class": "details"})
        if file_id_tag:
            file_id = file_id_tag.get('data-id')
    if not file_id:
        raise ValueError("file_id not found in the HTML response")


    payload = {
        "fid" : file_id,
        "share_key": share_key, 
    }
    
    initial_response = session.post("https://www.febbox.com/file/player", headers=initial_headers, data=payload, cookies=cookies, proxies=proxies).text
    
    pattern = r'var\s+sources\s*=\s*(\[.*?\]);'

    match = re.search(pattern, initial_response)
    json_response = json.loads(match.group(1))
    unique_qualities = {}
    valid_qualities = ['4K', '1080P', '720P', '480P', '360P', '240P', '144P']
    filtered_files = {}
    
    for source in json_response:
        quality = source['label']
        file_url = source.get('file')
        if quality in valid_qualities:
            if file_url:
                filtered_files[quality.lower()] = file_url
        elif quality == 'ORG':
            if file_url:
                for q in valid_qualities:
                    if q.lower() in file_url.lower():
                        filtered_files[q.lower()] = file_url
                        break
    
    response_data['status'] = 'success'
    response_data['status_code'] = 200
    response_data['streaming_urls'] = filtered_files
    response_data['downloading_urls'] = filtered_files
    return response_data

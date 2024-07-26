import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
import json

default_domain = "https://antol307vvk.com"
initial_headers = {
    'Referer': default_domain,
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

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

#Create session
session = requests.Session()
session.proxies.update(proxy)

qualities= ['144', '240', '360', '480', '720', '1080']

def real_extract(url):
    #Get initial embed page
    initial_response = session.get(url, headers=initial_headers).text
    #Get first playlist URL
    match = re.search(r'"file":"([^"]+)"', initial_response)
    url = match.group(1).replace('\\/', '/')
    #Get X-CSRF-TOKEN
    match = re.search(r'"key":"([^"]+)"', initial_response)
    key = match.group(1).replace('\\/', '/')
    #Set token to headers
    initial_headers['X-CSRF-TOKEN'] = key
    #Create complete playlist URL
    url = default_domain + url
    initial_response = session.post(url, headers=initial_headers)
    #Convert response to JSON
    data = json.loads(initial_response.text)
    #Extract Hindi language playlist URL
    hindi_file = next((item['file'] for item in data if item['title'] == 'Hindi'), None)
    cleaned_file = hindi_file.replace('~', '')
    url = f'{default_domain}/playlist/{cleaned_file}.txt'
    #Make request to the URL
    initial_response = session.post(url, headers=initial_headers)
    #Make request to lang playlist
    initial_response = session.post(initial_response.text, headers=initial_headers)
    redirected_url = initial_response.url
    url = redirected_url.rsplit('/', 1)[0]
    lines = initial_response.text.splitlines()

    streaming_urls = {}
    for quality in qualities:
        if quality in initial_response.text:
            quality_url = f"{url}/{quality}/index.m3u8"
            streaming_urls[f"{quality}p"] = quality_url
    response_data['status'] = 'success'
    response_data['status_code'] = 200
    response_data['streaming_urls'] = streaming_urls
    return response_data
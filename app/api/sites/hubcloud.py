import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
import json

default_domain = "https://hubcloud.club"
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
#session.proxies.update(proxy)

qualities= ['144p', '240p', '360p', '480p', '720p', '1080p']

def real_extract(url):
    #Get initial download page
    initial_response = session.get(url, headers=initial_headers).text
    soup = BeautifulSoup(initial_response, "html.parser")
    anchor_tag = soup.find("a", attrs={"class": "btn"})
    next_page_url = None
    if anchor_tag:
        next_page_url = anchor_tag['href']
    
    initial_response = session.get(next_page_url, headers=initial_headers).text
    soup = BeautifulSoup(initial_response, "html.parser")
    anchor_tags = soup.find_all("a", attrs={"class": "btn"})
    media_url = None
    media_urls = {}
    for anchor_tag in anchor_tags:
        if "Download File" in anchor_tag.text:
            media_url = anchor_tag['href']
    
    for quality in qualities:
        if quality in media_url:
            media_urls[f"{quality}"] = media_url
    response_data['status'] = 'success'
    response_data['status_code'] = 200
    response_data['streaming_urls'] = media_urls
    response_data['downloading_urls'] = media_urls
    return response_data
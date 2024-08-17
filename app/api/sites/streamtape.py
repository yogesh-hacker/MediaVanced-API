import requests
from django.http import JsonResponse
import re

default_domain = "https://streamtape.com"
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

#Create session
session = requests.Session()

qualities= ['144p', '240p', '360p', '480p', '720p', '1080p','2160p']

def real_extract(url):
    initial_response = session.get(url, headers=initial_headers).text
    regex_pattern = r"document\.getElementById\(['\"]captchalink['\"]\)\.innerHTML\s*=\s*['\"]([^'\"]+)['\"].*?\+\s*\(['\"]([^'\"]+)['\"]\)\.substring\(\d+\);"
    botlink_match = re.search(regex_pattern, initial_response)
    if botlink_match is None:
        response_data['status'] = 'failed'
        response_data['status_code'] = 200
        response_data['error'] = "Unable to locate media URLs, likely because they have been deleted!"
        return response_data
    streaming_url = "https:" + botlink_match.group(1) + botlink_match.group(2)[4:]
    final_response = session.get(streaming_url, headers=initial_headers, allow_redirects=False)
    media_url = final_response.headers.get('Location')
    available_quality = next((q for q in qualities if q in media_url), "UNKNOWN")
    quality_key = f"{available_quality}p" if available_quality != "UNKNOWN" else "UNKNOWN"
    media_urls = {quality_key: media_url}
    response_data['status'] = 'success'
    response_data['status_code'] = 200
    response_data['streaming_urls'] = media_urls
    response_data['downloading_urls'] = media_urls
    return response_data
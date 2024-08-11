import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from django.http import JsonResponse
import random
import time

# Default domain and initial headers for the requests
default_domain = "https://photojin.online/"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

# Initialize session for making requests
session = requests.Session()

def real_extract(url):
    """
    Extractor Entry Point
    """
    response_data = {
        'status': None,
        'status_code': None,
        'error': None,
        'headers': {},
        'streaming_urls': {},
        'downloading_urls': {}
    }

    try:
        # Get initial response from the URL
        initial_response = session.get(url, headers=initial_headers)
        if initial_response.status_code != 200:
            response_data['status'] = 'falied'
            response_data['status_code'] = initial_response.status_code
            response_data['error'] = 'Failed to fetch initial page, may be default domain changed, ask admin to configure'
            return response_data
            
        parsed_url = urlparse(initial_response.url)
        default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        
        # Parse the HTML content
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        data_field = soup.find("section", id="generate_url")
        
        # Extract quality information
        quality = None
        quality_options = ['1080p', '720p', '480p', '360p']
        for option in quality_options:
            if option in initial_response.text:
                quality = option
                break

        if not quality:
            quality = "UNKNOWN"

        # Prepare data for the POST request
        data = {
            "type": "DOWNLOAD_GENERATE",
            "payload": {
                "uid": data_field['data-uid'],
                "access_token": data_field['data-token']
            }
        }

        json_data = json.dumps(data)
        headers = {
            "X-Requested-With": "xmlhttprequest"
        }

        # Make the POST request to generate the download URL
        post_response = session.post(f"{default_domain}action", data=json_data, headers=headers)
        if post_response.status_code != 200:
            response_data['status'] = 'falied'
            response_data['status_code'] = post_response.status_code
            response_data['error'] = 'Failed to generate download URL, check if default_domain is correctly configure'
            return response_data

        post_response_json = post_response.json()
        captured_url = post_response_json['download_url']
        
        # Populate response data
        response_data['status'] = 'success'
        response_data['status_code'] = 200
        response_data['streaming_urls'][quality] = captured_url
        response_data['downloading_urls'][quality] = captured_url

    except Exception as e:
        response_data['status'] = 'error'
        response_data['status_code'] = 500
        response_data['error'] = str(e)

    return response_data

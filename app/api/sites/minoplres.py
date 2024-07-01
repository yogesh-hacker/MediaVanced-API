import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse

default_domain = "https://minoplres.xyz/"
initial_headers = {
    'Origin': default_domain,
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

base_url = "https://minoplres.xyz/d/l1s6pevitg6y_{}"
suffixes = ['h', 'l', 'o']
qualities = {
    'h': '720p',
    'l': '360p',
    'o': '480p'
}

def real_extract(url):
    response_data = {
        'status': None,
        'status_code': None,
        'error': None,
        'headers': {},
        'streaming_urls': {},
        'downloading_urls': {}
    }

    try:
        # Streaming URL extraction
        initial_response = requests.get(url, headers=initial_headers)
        print(initial_response.request.headers)
        print(initial_response)
        initial_response.raise_for_status()  # Raise an HTTPError if the response was unsuccessful
        initial_page_html = initial_response.text

        stream_pattern = r'file:"([^"]+)"'
        stream_match = re.search(stream_pattern, initial_page_html)
        
        if stream_match:
            stream_url_base = stream_match.group(1)
            stream_url_template = re.sub(r'(_[a-z])', '_{}', stream_url_base)
            for suffix in suffixes:
                quality = qualities.get(suffix, 'unknown')
                stream_url = stream_url_template.format(suffix)
                stream_response = requests.get(stream_url, headers=initial_headers)
                if stream_response.status_code == 200:
                    response_data['streaming_urls'][quality] = stream_url
        else:
            response_data['error'] = 'Regex error, failed to extract streaming URL!'

        # Downloading URL extraction
        headers = {
            "Referer": "https://minoplres.xyz/"
        }

        for suffix in suffixes:
            download_url = base_url.format(suffix)
            response = requests.get(download_url, headers=headers)
            
            if "This version" not in response.text:
                mPageHtml = response.text
                mSoup = BeautifulSoup(mPageHtml, "html.parser")
                mOp = mSoup.find("input", attrs={"name": "op"})
                mId = mSoup.find("input", attrs={"name": "id"})
                mMode = mSoup.find("input", attrs={"name": "mode"})
                mHash = mSoup.find("input", attrs={"name": "hash"})
                
                payload = {
                    "op": mOp['value'],
                    "id": mId['value'],
                    "mode": mMode['value'],
                    "hash": mHash['value']
                }
                
                mResponse2 = requests.post(download_url, data=payload, headers=headers)
                mPageHtml2 = mResponse2.text
                mPattern = r'href="([^"]+\.mp4[^"]*)"'
                mMatch = re.search(mPattern, mPageHtml2)
                if mMatch:
                    quality = qualities.get(suffix, 'unknown')
                    response_data['downloading_urls'][quality] = mMatch.group(1)
            #else:
                #response_data['error'] = f'Request to {download_url} failed because: QUALITY UNAVAILABLE'

        if not response_data['streaming_urls'] and not response_data['downloading_urls']:
            response_data['status'] = 'failed'
            response_data['status_code'] = 500
        else:
            response_data['status'] = 'success'
            response_data['status_code'] = 200

        response_data['headers']['Referer'] = default_domain
        return response_data
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Request error: {str(e)}', 'status_code': 500}
    
    except re.error as e:
        return {'error': f'Regex error: {str(e)}', 'status_code': 500}
    
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}', 'status_code': 500}
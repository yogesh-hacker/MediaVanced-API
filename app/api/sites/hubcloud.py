import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse

# Constants and setup
default_domain = "https://hubcloud.club"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}
proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}
qualities = ['144p', '240p', '360p', '480p', '720p', '1080p']

# Response data template
response_data = {
    'status': None,
    'status_code': None,
    'error': None,
    'headers': {},
    'streaming_urls': {},
    'downloading_urls': {}
}

# Create session with optional proxy
session = requests.Session()
# session.proxies.update(proxy)

def real_extract(url):
    try:
        # Initial request to get the download page
        initial_response = session.get(url, headers=initial_headers).text

        # Check for redirect
        if "Redirect" in initial_response:
            soup = BeautifulSoup(initial_response, "html.parser")
            meta_tag = soup.find("meta", attrs={"http-equiv": "refresh"})
            if meta_tag and 'content' in meta_tag.attrs:
                redirect_url = meta_tag['content'].split("url=")[-1]
                if not redirect_url.startswith("http"):
                    redirect_url = f"{default_domain}{redirect_url}"
                initial_response = session.get(redirect_url, headers=initial_headers).text

        # Extract URL pattern
        url_pattern = r"https:\/\/[^'\" ]*hubcloud\.php[^'\" ]*\b(id=[^&]+&token=[^'\" ]+|token=[^&]+&id=[^'\" ]+)"
        match = re.search(url_pattern, initial_response)
        next_page_url = match.group(0) if match else None

        # Validate the next page URL
        if next_page_url is None:
            response_data.update({
                'status': 'failed',
                'status_code': 404,
                'error': 'Could not locate download link',
            })
            return response_data

        # Ensure the URL includes scheme
        if not next_page_url.startswith("http"):
            next_page_url = f"{default_domain}/{next_page_url}"

        # Get the page with download links
        initial_response = session.get(next_page_url, headers=initial_headers).text
        soup = BeautifulSoup(initial_response, "html.parser")

        # Extract media URLs based on quality
        anchor_tags = soup.find_all("a", attrs={"class": "btn"})
        media_urls = {}
        for anchor_tag in anchor_tags:
            if "Download File" in anchor_tag.text:
                media_url = anchor_tag['href']
                for quality in qualities:
                    if quality in media_url:
                        media_urls[quality] = media_url

        # Check if we found any media URLs
        if not media_urls:
            response_data.update({
                'status': 'failed',
                'status_code': 404,
                'error': 'No downloadable media links found'
            })
            return response_data

        # Success response
        response_data.update({
            'status': 'success',
            'status_code': 200,
            'streaming_urls': media_urls,
            'downloading_urls': media_urls
        })
        return response_data

    except requests.RequestException as e:
        # Catch network errors and log the exception
        response_data.update({
            'status': 'error',
            'status_code': 500,
            'error': str(e)
        })
        return response_data

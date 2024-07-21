import requests
import re
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin


default_domain = "https://febbox.com/"
initial_headers = {
    "Referer": default_domain,
    "User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

cookies = {
    "cf_clearance" : "7EMvhCoJXzLoB95qoypKRxLaPwEPPMQ_lxNTrZXUgHg-1718419969-1.0.1.1-MDMXbyRum_hdlG34Ovqctc_8sHoWFCS1PMa1xp17Rwydf_uZWwRYnKdeTUprNRxfkExtOm6K_rJPxHzeKOc4KQ"
}

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

response_data = {
    'status': None,
    'status_code': None,
    'error': None,
    'headers': {},
    'streaming_urls': {},
    'downloading_urls': {}
}

qualities= ['144', '240', '360', '480', '720', '1080']

def fetch_and_construct_urls(initial_response):
    base_url = initial_response.url.rsplit('/', 1)[0] + '/'
    streaming_urls = {}
    for quality in qualities:
        if quality in initial_response.text:
            quality_url = f"{base_url}{quality}.mp4"
            streaming_urls[f"{quality}p"] = quality_url
    return streaming_urls


def real_extract(url):
    """
    Extractor Entry Point
    """
    initial_response = requests.get(url, headers=initial_headers, cookies=cookies)
    initial_page_html = initial_response.text
    soup = BeautifulSoup(initial_page_html,"html.parser")
    iframe = soup.find("div", attrs={"class": "player-iframe"})
    script = iframe.find_all("script")
    pattern = r'atob\("([^"]*)"\)'
    matcher = re.search(pattern, script[1].string)
    if matcher:
        encoded_data = matcher.group(1);
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_string = decoded_bytes.decode('utf-8')
        pattern = r'file:"([^"]+)"'
        matcher = re.search(pattern, decoded_string)
        if matcher:
            initial_response = requests.get(matcher.group(1), headers=initial_headers, proxies=proxy)
            streaming_urls = fetch_and_construct_urls(initial_response)
            #Return response
            response_data['status'] = 'success'
            response_data['status_code'] = 200
            response_data['streaming_urls'] = streaming_urls
            response_data['downloading_urls'] = streaming_urls
            return response_data;
        else:
            response_data['status'] = 'failed'
            response_data['status_code'] = 500
            response_data['error'] = "Unable to locate media URL."
    else:
        response_data['status'] = 'failed'
        response_data['status_code'] = 500
        response_data['error'] = "Unable to locate ciphered text conatining media URL."
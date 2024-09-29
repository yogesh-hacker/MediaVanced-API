import requests
import re

default_domain = "https://www.dailymotion.com"
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

# Create session
session = requests.Session()
session.proxies.update(proxy)

def _re_construct(url):
    pattern = r"https://www\.dailymotion\.com/(video|embed)/(?P<video_id>[^/?]+)"
    
    match = re.search(pattern, url)
    
    if match:
        video_id = match.group('video_id')
        new_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
        return new_url
    else:
        raise ValueError("URL format is not recognized")


def real_extract(url):
    url = _re_construct(url)
    # Get video metadata
    initial_response = session.get(url, headers=initial_headers)
    
    # Get first playlist URL (auto quality)
    json_content = initial_response.json()
    playlist_url = json_content["qualities"]["auto"][0]["url"]
    
    # Get playlist response
    playlist_response = session.get(playlist_url, headers=initial_headers).text
    
    # Get each quality URL
    pattern = re.compile(r'NAME="(\d+)".*?PROGRESSIVE-URI="(.*?)".*?\s(https://\S+)')
    matches = pattern.findall(playlist_response)

    # Collect the URLs in a list and sort by resolution (low to high)
    sorted_matches = sorted(matches, key=lambda x: int(x[0]))
    
    # Extracted URLs and Resolutions
    streaming_urls = {}
    downloading_urls = {}

    for match in sorted_matches:
        resolution = match[0]
        downloading_url = match[1]
        streaming_url = match[2]
        streaming_urls[f"{resolution}p"] = streaming_url
        downloading_urls[f"{resolution}p"] = downloading_url
    
    response_data['status'] = 'success'
    response_data['status_code'] = 200
    response_data['streaming_urls'] = streaming_urls
    response_data['downloading_urls'] = downloading_urls
    
    return response_data

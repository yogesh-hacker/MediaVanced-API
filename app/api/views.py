from django.http import JsonResponse
from .sites import minoplres, photojin, febbox, saicord, antol, streamtape

def api_endpoint(request):
    target_url = request.GET.get('url', None)
    
    if target_url is None:
        return JsonResponse({'error': 'URL parameter "url" is required'}, status=400)
    
    if "minoplres" in target_url:
        data = minoplres.real_extract(target_url)
    elif "photojin" in target_url:
        data = photojin.real_extract(target_url)
    elif "febbox" in target_url:
        data = febbox.real_extract(target_url)
    elif "saicord" in target_url:
        data = saicord.real_extract(target_url)
    elif "antol" in target_url:
        data = antol.real_extract(target_url)
    elif "streamtape" in target_url:
        data = streamtape.real_extract(target_url)
    else:
        return JsonResponse({'error': 'Invalid site name'}, status=400)

    if not isinstance(data, dict):
        data = {'error': 'Unexpected error: invalid response from real_extract'}
    return JsonResponse(data, status=data.get('status_code', 200))
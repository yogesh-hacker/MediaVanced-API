from django.http import JsonResponse
from .sites import minoplres, photojin, febbox, saicord, antol, streamtape, hubcloud, dailymotion

# List of extractors with corresponding domains
site_extractors = [
    (['minoplres', 'speedostream'], minoplres),
    (['photojin'], photojin),
    (['febbox'], febbox),
    (['saicord'], saicord),
    (['antol'], antol),
    (['streamtape'], streamtape),
    (['hubcloud'], hubcloud),
    (['dailymotion'], dailymotion),
]

def api_endpoint(request):
    target_url = request.GET.get('url', None)
    
    if not target_url:
        return JsonResponse({'error': 'URL parameter "url" is required'}, status=400)
    
    for domains, extractor in site_extractors:
        if any(domain in target_url for domain in domains):
            data = extractor.real_extract(target_url)
            break
    else:
        return JsonResponse({'error': 'Invalid site name'}, status=400)
    
    if not isinstance(data, dict):
        data = {'error': 'Unexpected error: invalid response from real_extract'}

    return JsonResponse(data, status=data.get('status_code', 200))

from django.http import JsonResponse
from .sites import minoplres

def api_endpoint(request):
    target_url = request.GET.get('url', None)
    
    if target_url is None:
        return JsonResponse({'error': 'URL parameter "url" is required'}, status=400)
    
    if "minoplres" in target_url:
        data = minoplres.real_extract(target_url)
    else:
        return JsonResponse({'error': 'Invalid site name'}, status=400)

    if not isinstance(data, dict):
        data = {'error': 'Unexpected error: invalid response from real_extract'}

    return JsonResponse(data, status=data.get('status_code', 200))
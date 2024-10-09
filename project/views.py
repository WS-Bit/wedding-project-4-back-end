from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def enter_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('password') == settings.SITE_PASSWORD:
            request.session['is_authenticated'] = True
            return JsonResponse({'is_authenticated': True})
        else:
            return JsonResponse({'is_authenticated': False}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def home(request):
    if not request.session.get('is_authenticated'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    return JsonResponse({'message': 'Welcome to the home page'})
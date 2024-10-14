from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/api/csrf_cookie/', '/api/enter_password/']:
            return self.get_response(request)
        
        if not request.session.get('is_authenticated'):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        return self.get_response(request)
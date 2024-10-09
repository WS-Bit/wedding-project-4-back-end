from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('is_authenticated'):
            # Allow access to the password entry endpoint
            if request.path == reverse('enter_password'):
                return self.get_response(request)
            
            # For API requests, return a JSON response instead of redirecting
            if request.path.startswith('/api/'):
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # For non-API requests, redirect to the password entry page
            return redirect('enter_password')
        
        return self.get_response(request)
import logging
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.middleware.csrf import get_token

logger = logging.getLogger(__name__)

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:  # Skip authentication in development
            return self.get_response(request)

        # Always allow CSRF token requests
        if request.path == '/api/csrf_cookie/':
            get_token(request)  # This sets the CSRF cookie
            return self.get_response(request)

        if not request.session.get('is_authenticated'):
            # Allow access to the password entry endpoint
            if request.path == reverse('enter_password'):
                return self.get_response(request)
            
            # For API requests, check CSRF token and return JSON response
            if request.path.startswith('/api/'):
                csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
                cookie_token = request.COOKIES.get('csrftoken')
                logger.debug(f"CSRF Token in header: {csrf_token}")
                logger.debug(f"CSRF Token in cookie: {cookie_token}")
                
                if csrf_token and csrf_token == cookie_token:
                    # CSRF token is valid, but user is not authenticated
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                else:
                    # Invalid or missing CSRF token
                    return JsonResponse({'error': 'CSRF verification failed'}, status=403)
            
            # For non-API requests, redirect to the password entry page
            return redirect('enter_password')
        
        return self.get_response(request)
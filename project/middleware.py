from django.shortcuts import redirect
from django.urls import reverse

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('is_authenticated'):
            if request.path != reverse('enter_password'):
                return redirect('enter_password')
        return self.get_response(request)
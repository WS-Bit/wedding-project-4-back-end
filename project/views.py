from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

from django.conf import settings

from django.views.decorators.csrf import ensure_csrf_cookie
import logging

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})



@require_POST
@ensure_csrf_cookie
def enter_password(request):
    password = request.POST.get('password')
    if password == settings.SITE_PASSWORD:
        request.session['is_authenticated'] = True
        request.session.save()
        return JsonResponse({'is_authenticated': True})
    return JsonResponse({'is_authenticated': False, 'error': 'Incorrect password'}, status=401)
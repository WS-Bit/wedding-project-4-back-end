from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@require_GET
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def set_csrf_token(request):
    logger.info(f"Setting CSRF cookie. Current cookies: {request.COOKIES}")
    response = JsonResponse({"details": "CSRF cookie set"})
    logger.info(f"Response cookies: {response.cookies}")
    return response

@require_POST
@ensure_csrf_cookie
def enter_password(request):
    password = request.POST.get('password')
    if password == settings.SITE_PASSWORD:
        request.session['is_authenticated'] = True
        request.session.save()
        return JsonResponse({'is_authenticated': True})
    return JsonResponse({'is_authenticated': False, 'error': 'Incorrect password'}, status=401)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class EnterPasswordView(APIView):
    def post(self, request):
        try:
            logger.info("Received password entry request")
            logger.debug(f"Request headers: {request.headers}")
            
            data = request.data
            logger.debug(f"Request data: {data}")
            
            if 'password' not in data:
                logger.error("Password field missing in request data")
                return Response({'error': 'Password field is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if data.get('password') == settings.SITE_PASSWORD:
                request.session['is_authenticated'] = True
                logger.info("Password correct, authentication successful")
                return Response({'is_authenticated': True})
            else:
                logger.warning("Incorrect password entered")
                return Response({'is_authenticated': False, 'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Unexpected error in EnterPasswordView: {str(e)}")
            logger.exception("Exception details:")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
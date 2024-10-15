import jwt
import json
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def enter_password(request):
    password = json.loads(request.body).get('password')
    if password == settings.SITE_PASSWORD:
        # Generate JWT token
        payload = {
            'authenticated': True,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({'is_authenticated': True, 'token': token})
    return JsonResponse({'is_authenticated': False, 'error': 'Incorrect password'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_status(request):
    return JsonResponse({'isAuthenticated': True})
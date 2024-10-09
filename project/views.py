from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EnterPasswordView(APIView):
    def post(self, request):
        password = request.data.get('password')
        if password == settings.SITE_PASSWORD:
            request.session['is_authenticated'] = True
            request.session.save()
            logger.info(f"Authentication successful. Session ID: {request.session.session_key}")
            return Response({'is_authenticated': True}, status=status.HTTP_200_OK)
        logger.warning(f"Authentication failed. Provided password: {password}")
        return Response({'is_authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)
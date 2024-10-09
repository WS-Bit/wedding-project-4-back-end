import logging
import traceback
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Guest
from .serializers.common import GuestSerializer
from phonenumber_field.phonenumber import PhoneNumber

logger = logging.getLogger(__name__)

class GuestView(APIView):
    def check_authentication(self, request):
        logger.info(f"Session data: {dict(request.session)}")
        if not request.session.get('is_authenticated'):
            logger.warning("Authentication check failed")
            raise PermissionDenied("Authentication required")
        logger.info("Authentication check passed")

    def post(self, request):
        logger.info(f"Received POST request with data: {request.data}")
        try:
            self.check_authentication(request)
            
            # Convert phone number to PhoneNumber instance
            phone = request.data.get('phone')
            if phone:
                try:
                    request.data['phone'] = PhoneNumber.from_string(phone).as_e164
                except Exception as e:
                    logger.error(f"Error processing phone number: {str(e)}")
                    return Response({"error": f"Invalid phone number: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            guest_to_add = GuestSerializer(data=request.data)
            if guest_to_add.is_valid():
                guest = guest_to_add.save()
                request.session['guest_id'] = guest.id
                logger.info(f"Guest created with id: {guest.id}")
                return Response(guest_to_add.data, status=status.HTTP_201_CREATED)
            logger.error(f"Invalid data: {guest_to_add.errors}")
            return Response(guest_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return Response({"error": str(e), "traceback": traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
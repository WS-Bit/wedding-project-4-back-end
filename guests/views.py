import logging
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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

    def get(self, request):
        logger.info("Received GET request for guests")
        try:
            self.check_authentication(request)
            guests = Guest.objects.all()
            serializer = GuestSerializer(guests, many=True)
            logger.info(f"Returning {len(guests)} guests")
            return Response(serializer.data)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(f"Unexpected error in GET request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    return Response({"phone": [f"Invalid phone number: {str(e)}"]}, status=status.HTTP_400_BAD_REQUEST)

            guest_to_add = GuestSerializer(data=request.data)
            if guest_to_add.is_valid():
                try:
                    guest = guest_to_add.save()
                    request.session['guest_id'] = guest.id
                    logger.info(f"Guest created with id: {guest.id}")
                    return Response(guest_to_add.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if 'email' in str(e).lower():
                            return Response({"email": ["This email is already registered."]}, status=status.HTTP_400_BAD_REQUEST)
                        elif 'phone' in str(e).lower():
                            return Response({"phone": ["This phone number is already registered."]}, status=status.HTTP_400_BAD_REQUEST)
                    logger.error(f"IntegrityError: {str(e)}")
                    return Response({"error": "An error occurred while saving the guest."}, status=status.HTTP_400_BAD_REQUEST)
                except ValidationError as e:
                    logger.error(f"ValidationError: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            logger.error(f"Invalid data: {guest_to_add.errors}")
            return Response(guest_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from djoser.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

User = get_user_model()

class CustomPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk)) # Hash the user id to make it safe to send in the email link
        token = default_token_generator.make_token(user) # Generate the token that will be sent in the email link

        reset_url = settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid, token=token)

        return Response({
            "reset_url": reset_url,
            "uid": uid,
            "token": token
        }, status=status.HTTP_200_OK)
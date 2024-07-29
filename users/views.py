from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from djoser.conf import settings as djoser_settings
from django.conf import settings as django_settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	TokenVerifyView,
)

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

        reset_url = djoser_settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid, token=token)

        return Response({
            "reset_url": reset_url,
            "uid": uid,
            "token": token
        }, status=status.HTTP_200_OK)
	
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data['access']
            response.set_cookie(
				key='access',
				value=access,
				max_age=django_settings.AUTH_COOKIE_ACCESS_MAX_AGE,
				secure=django_settings.AUTH_COOKIE_SECURE,
				httponly=django_settings.AUTH_COOKIE_HTTP_ONLY,
				samesite=django_settings.AUTH_COOKIE_SAMESITE,
				path=django_settings.AUTH_COOKIE_PATH
			)
            refresh = response.data['refresh']
            response.set_cookie(
                key='refresh',
                value=refresh,
                max_age=django_settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                secure=django_settings.AUTH_COOKIE_SECURE,
                httponly=django_settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=django_settings.AUTH_COOKIE_SAMESITE,
                path=django_settings.AUTH_COOKIE_PATH
			)
        return response
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh')
        if refresh:
            request.data['refresh'] = refresh # Set the refresh token in the request data so that the parent class can use it to generate a new access token.
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data['access']
            response.set_cookie(
				key='access',
				value=access,
				max_age=django_settings.AUTH_COOKIE_ACCESS_MAX_AGE,
				secure=django_settings.AUTH_COOKIE_SECURE,
				httponly=django_settings.AUTH_COOKIE_HTTP_ONLY,
				samesite=django_settings.AUTH_COOKIE_SAMESITE,
				path=django_settings.AUTH_COOKIE_PATH
			)
        return response

class CustomTokenVerifyView(TokenVerifyView):
	def post(self, request, *args, **kwargs):
		access = request.COOKIES.get('access')
		if access:
			request.data['token'] = access # Set the access token in the request data so that the parent class can use it to verify the token.
		return super().post(request, *args, **kwargs)

class LogoutView(APIView):
	def post(self, request):
		response = Response(status=status.HTTP_204_NO_CONTENT)
		response.delete_cookie('access')
		response.delete_cookie('refresh')
		return response


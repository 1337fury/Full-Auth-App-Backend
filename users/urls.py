from django.urls import path
from .views import (
    CustomUserViewSet,
    CustomPasswordResetView,
	CustomTokenObtainPairView,
	CustomTokenRefreshView,
	CustomTokenVerifyView,
	LogoutView
)

urlpatterns = [
	path('users/me/', CustomUserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
	path('custom-password-reset/', CustomPasswordResetView.as_view(), name='custom-password-reset'),
	path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
	path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
	path('jwt/verify/', CustomTokenVerifyView.as_view(), name='jwt-verify'),
	path('logout/', LogoutView.as_view(), name='logout')
]
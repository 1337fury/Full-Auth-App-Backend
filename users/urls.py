from django.urls import path
from users.views import CustomUserViewSet
from users.views import CustomPasswordResetView

urlpatterns = [
	path('users/me/', CustomUserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
	path('custom-password-reset/', CustomPasswordResetView.as_view(), name='custom-password-reset'),
]
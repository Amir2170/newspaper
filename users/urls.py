from django.urls import path

from .views import SignUpView, CustomPasswordResetView


urlpatterns = [
	path('password_reset/', CustomPasswordResetView.as_view(), name='passwordreset'),
	path('signup/', SignUpView.as_view(), name='signup'),
]

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
	
	form_class = CustomUserCreationForm
	
	success_url = reverse_lazy('login')
	
	template_name = 'signup.html'


class CustomPasswordResetView(PasswordResetView):
	
	from_email = 'newspaper2170@gmail.com'
	

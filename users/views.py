from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.utils.decorators import method_decorator

from .forms import CustomUserCreationForm

csrf_token_decorators = [requires_csrf_token, csrf_exempt]
@method_decorator(csrf_token_decorators, name='dispatch')
class SignUpView(CreateView):
	
	form_class = CustomUserCreationForm
	
	success_url = reverse_lazy('login')
	
	template_name = 'signup.html'


class CustomPasswordResetView(PasswordResetView):
	
	from_email = 'newspaper2170@gmail.com'
	

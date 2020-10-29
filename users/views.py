from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .forms import CustomUserCreationForm


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(CreateView):
	
	form_class = CustomUserCreationForm
	
	success_url = reverse_lazy('login')
	
	template_name = 'signup.html'


class CustomPasswordResetView(PasswordResetView):
	
	from_email = 'newspaper2170@gmail.com'
	

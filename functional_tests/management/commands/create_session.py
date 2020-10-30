from django.conf import settings
from django.contrib.auth import (
	BACKEND_SESSION_KEY, 
	SESSION_KEY, 
	get_user_model,
	HASH_SESSION_KEY
)
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


def create_pre_authenticated_session(username, password):
	user = User.objects.create_user(username=username, password=password)
	session = SessionStore()
	session[SESSION_KEY] = user.pk
	session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
	session[HASH_SESSION_KEY] = user.get_session_auth_hash()
	session.save()
	return session.session_key
	
class Command(BaseCommand):
	
	def add_arguments(self, parser):
		parser.add_argument('username')
		parser.add_argument('password')
	
	def handle(self, *args, **options):
		username = options['username']
		password = options['password']
		session_key = create_pre_authenticated_session(username, password)
		self.stdout.write(session_key)


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from unittest.mock import patch
import os

User = get_user_model()


class LoginViewTest(TestCase):
	
	def test_login_logout_process(self):
		user = User.objects.create_user(username='testuser', password='1234')
		logged_in = self.client.login(username='testuser', password='1234')
		self.assertTrue(logged_in)
	
	def test_login_page_uses_correct_template(self):
		response = self.client.get(reverse('login'))
		self.assertTemplateUsed(response, 'registration/login.html')
		

class LogoutViewTest(TestCase):
	
	def test_logout_process(self):
		user = User.objects.create_user(username='testuser', password='1234')
		self.client.login(username='testuser', password='1234')
		response = self.client.get(reverse('logout'))
		self.assertRedirects(response, reverse('home'))


class SignUpViewTest(TestCase):
	
	def test_signup_page_uses_correct_template(self):
		response = self.client.get(reverse('signup'))
		self.assertTemplateUsed(response, 'signup.html')
		
	def test_signup_form(self):
		User.objects.create_user(username='testuser', email='test@user.com')
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(User.objects.all()[0].username, 'testuser')
		self.assertEqual(User.objects.all()[0].email, 'test@user.com')


class PasswordChnageTest(TestCase):
	
	def test_password_change_uses_right_view(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.get('/users/password_change/')
		self.assertTemplateUsed(response, 'registration/password_change_form.html')
		

class PasswordDoneTest(TestCase):
	
	def test_password_change_done_uses_correct_template(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.get('/users/password_change/done/')
		self.assertTemplateUsed(response, 'registration/password_change_done.html')


class CustomPasswordResetViewTest(TestCase):
	
	@patch('users.views.CustomPasswordResetView.form_class.send_mail')
	def test_password_reset_flow(self, mock_send_mail):
		User.objects.create(username='testuser', email='a@b.com')
		self.client.post(reverse('passwordreset'), data={
			'email': 'a@b.com'} , follow=True
		)
		
		args1, args2  = mock_send_mail.call_args
		
		self.assertTrue(mock_send_mail.called)
		self.assertEqual(args1[3], 'newspaper2170@gmail.com')
		self.assertEqual(args1[4], 'a@b.com')
		

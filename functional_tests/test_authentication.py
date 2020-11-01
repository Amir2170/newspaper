from .base import FunctionalTest
from selenium import webdriver
import time
from django.core import mail
import re
import os
import poplib


class TestAuthentication(FunctionalTest):
	
	def wait_for_email(self, test_email, subject):
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body
		
		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com')
		try:
			inbox.user(test_email)
			inbox.pass_(os.environ['GMAIL_PASSWORD'])
			while time.time() - start < 60:
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting message ', i)
					_, lines, _ = inbox.retr(i)
					lines = [l.decode('utf8') for l in lines]
					print(lines)
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()
		
		
	def test_signup_login_logout(self):
		# martin goes to homepage of the newspaper site
		self.browser.get(self.live_server_url)
		
		# he tries to signup
		self.browser.find_element_by_link_text('Sign up').click()
		
		# he gets to the signup page so he enters his information
		self.browser.find_element_by_id('id_username').send_keys('testuser')
		self.browser.find_element_by_id('id_email').send_keys('newspaper2170@gmail.com')
		self.browser.find_element_by_id('id_age').send_keys('20')
		self.browser.find_element_by_id('id_password1').send_keys('mypass123')
		self.browser.find_element_by_id('id_password2').send_keys('mypass123')
		self.browser.find_element_by_tag_name('form button').click()
		self.wait_for(lambda: self.assertIn(
			'Log in',
			self.browser.find_element_by_link_text('h2').text
		))
		
		# he now gets redirected to the login page so he tries to login
		self.browser.find_element_by_id('id_username').send_keys('testuser')
		self.browser.find_element_by_id('id_password').send_keys('mypass123')
		self.browser.find_element_by_tag_name('form button').click()
		self.wait_for(lambda: self.assertIn(
			'Log out',
			self.browser.find_element_by_link_text('Log out').text
		))
		
		# he now tries to logout
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(lambda: self.assertIn(
			'Log in',
			self.browser.find_element_by_link_text('Log in').text
		))
		
	def test_reset_password(self):
		# martin goes to homepage of the newspaper site
		self.browser.get(self.live_server_url)
		
		# he tries to signup
		self.browser.find_element_by_link_text('Sign up').click()
		
		# he gets to the signup page so he enters his information
		self.browser.find_element_by_id('id_username').send_keys('testuser')
		self.browser.find_element_by_id('id_email').send_keys('newspaper2170@gmail.com')
		self.browser.find_element_by_id('id_age').send_keys('20')
		self.browser.find_element_by_id('id_password1').send_keys('mypass123')
		self.browser.find_element_by_id('id_password2').send_keys('mypass123')
		self.browser.find_element_by_tag_name('form button').click()
		self.wait_for(lambda: self.assertIn(
			'Log in',
			self.browser.find_element_by_link_text('h2').text
		))
			
		# he now remembers he just forgot his password so he goes to
		# the resert password page
		self.browser.find_element_by_link_text('Forget password?').click()
		self.browser.find_element_by_id('id_email').send_keys('newspaper2170@gmail.com')
		self.browser.find_element_by_id('email_button').click()
		self.wait_for(lambda: self.assertIn(
			'Check your inbox.',
			self.browser.find_element_by_tag_name('body').text
		))
		# he checks his email and finds a message
		body = self.wait_for_email('newspaper2170@gmail.com', 
			'Please reset your password'
		)
		self.assertIn(
			'click the button below to reset your password.', body.replace('\n',' ')
		)
		search_url = re.search('http://.+/.+/.+/.+/.+/', body)
		url = search_url.group()
		
		# he clicks on the link
		self.browser.get(url)
		
		# he gets to the page where he can change his password
		self.browser.find_element_by_id('id_new_password1').send_keys('mypass321')
		self.browser.find_element_by_id('id_new_password2').send_keys('mypass321')
		self.browser.find_element_by_id('new_password_button').click()
		
		# now they tries to login
		self.browser.find_element_by_link_text('Log in page').click()
		self.browser.find_element_by_id('id_username').send_keys('testuser')
		self.browser.find_element_by_id('id_password').send_keys('mypass321')
		self.browser.find_element_by_tag_name('form button').click()
		self.wait_for(lambda: self.assertIn(
			'Log out',
			self.browser.find_element_by_link_text('Log out').text
		))
			
		
		
		

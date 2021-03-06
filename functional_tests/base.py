from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import os

from .server_tools import reset_database


class FunctionalTest(StaticLiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.staging_server = os.environ.get('STAGING_SERVER')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server
			reset_database(self.staging_server)
		
	def tearDown(self):
		self.browser.quit()
	
	def wait(fn):
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			while True:
				try:
					return fn(*args, **kwargs)
				except(WebDriverException, AssertionError) as e:
					if time.time() - start_time > 5:
						raise e
		return modified_fn
	
	@wait
	def wait_for(self, fn):
		return fn 
		
		
		
		
		
		

from django.test import TestCase
from django.urls import reverse


class HomePageViewTest(TestCase):
	
	def test_homepage_uses_correct_template(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'home.html')

from .base import FunctionalTest
from django.conf import settings
from django.contrib.auth import ( 
	BACKEND_SESSION_KEY, 
	SESSION_KEY, 
	get_user_model, 
	HASH_SESSION_KEY
)
from django.contrib.sessions.backends.db import SessionStore
import time

User = get_user_model()


class TestAddingEditingDeletingAddingCommentAnArticle(FunctionalTest):
	
	def create_pre_authenticated_session(self, username, password):
		user = User.objects.create_user(username=username, password=password)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session[HASH_SESSION_KEY] = user.get_session_auth_hash()
		session.save()

		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key,
			path='/'
		))
		
	def test_can_add_edit_delete_add_comment_to_an_article(self):
		# johnny goes to the newspapersite, he is logged in
		self.create_pre_authenticated_session(username='testuser', password='mypass123')
		self.browser.get(self.live_server_url)
		
		# he sees a '+ New' link so he clicks on it
		self.browser.find_element_by_link_text('+ New').click()
		
		# then he gets to the article creating page so he fills the fields
		self.browser.find_element_by_id('id_title').send_keys('title')
		self.browser.find_element_by_id('id_body').send_keys('body')
		self.browser.find_element_by_id('button_new').click()
		self.wait_for(lambda: self.assertEqual(	
			'title',
			self.browser.find_element_by_tag_name('h2').text
		))
		
		# he now tries to edit his article
		self.browser.find_element_by_link_text('Edit').click()
		title = self.browser.find_element_by_id('id_title')
		title.clear()
		title.send_keys('updated title')
		body = self.browser.find_element_by_id('id_body')
		body.clear()
		body.send_keys('updated body')
		self.browser.find_element_by_id('edit_button').click()
		self.wait_for(lambda: self.assertEqual(	
			'updated title',
			self.browser.find_element_by_tag_name('h2').text
		))
		
		# he now tries to add a comment to his article
		self.browser.find_element_by_link_text('all articles').click()
		self.browser.find_element_by_link_text('Add comment').click()
		self.browser.find_element_by_id('id_comment').send_keys('comment')
		self.browser.find_element_by_id('new_comment_button').click()
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_class_name('font-weight-bold').text,
			'comment'
		))
		
		# he now tries to delete his article
		self.browser.find_element_by_link_text('Delete').click()
		self.browser.find_element_by_id('delete_button').click()
		self.wait_for(lambda: self.assertEqual(
			self.browser.current_url,
			self.live_server_url + 'articles/'
		))
		
		
		
		

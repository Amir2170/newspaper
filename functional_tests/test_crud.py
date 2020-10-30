from .base import FunctionalTest
from django.conf import settings
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
import time

User = get_user_model()


class TestAddingEditingDeletingAddingCommentAnArticle(FunctionalTest):
	
	def create_pre_authenticated_session(self, username, password):
		if self.staging_server:
			session_key = create_session_on_server(
				self.staging_server, username, password
			)
		else:
			session_key = create_pre_authenticated_session(username, password)
			
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
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
		
		
		
		

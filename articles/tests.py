from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Article, Comment
User = get_user_model()
	

class ArticleModelTest(TestCase):
	
	def test_can_create_a_model_with_right_fields(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
		title='article', body='first article', author=user
		)
		self.assertEqual(article.title, 'article')
		self.assertEqual(article.body, 'first article')
		self.assertEqual(article.author, user)
	
	def test_string_representation_of_model(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		self.assertEqual(str(article), 'article')
	
	def test_model_get_absolute_url(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		self.assertEqual(article.get_absolute_url(), reverse('article_detail',
			args=[str(article.id)]))
		

class CommentModelTest(TestCase):
	
	def test_model_has_right_fields(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
		title='article', body='first article', author=user
		)
		comment = Comment.objects.create( article=article, author=user,
			comment='first comment',
		)
		self.assertEqual(comment.article, article)
		self.assertEqual(comment.author, user)
		self.assertEqual(comment.comment, 'first comment')
	
	def test_string_representation_of_model(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
		title='article', body='first article', author=user
		)
		comment = Comment.objects.create( article=article, author=user,
			comment='first comment',
		)
		self.assertEqual(str(comment), comment.comment)
	
	def test_model_get_absolute_url(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		article = Article.objects.create(
		title='article', body='first article', author=user
		)
		comment = Comment.objects.create( article=article, author=user,
			comment='first comment',
		)
		self.assertEqual(comment.get_absolute_url(), reverse('article_list'))
		

class ArticleListViewTest(TestCase):
	
	def test_view_uses_right_template(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.get('/articles/')
		self.assertTemplateUsed(response, 'article_list.html')


class ArticleDetailViewTest(TestCase):
	
	def test_detail_page_uses_right_template(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		response = self.client.get(reverse('article_detail', 
			args=[str(article.id)]))
		self.assertTemplateUsed(response, 'article_detail.html')
		

class ArticleUpdateViewTest(TestCase):
	
	def test_update_view_uses_right_template(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		response = self.client.get(reverse('article_edit',
			args=[str(article.id)])
		)
		self.assertTemplateUsed(response, 'article_edit.html')
		
	def test_view_updates_an_existing_article(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='title', body='body', author=user
		)
		self.client.post(reverse('article_edit', args=[str(article.id)]), 
			data={ 'title': 'updated title', 'body': 'updated body', }
		)
		article.refresh_from_db()
		self.assertEqual(article.title, 'updated title')
		self.assertEqual(article.body, 'updated body')
		
	def test_post_redirects_to_detail_page(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='title', body='body', author=user
		)
		response = self.client.post(reverse('article_edit', 
			args=[str(article.id)]), 
			data={ 'title': 'updated title', 'body': 'updated body', }
		)
		self.assertRedirects(response, reverse('article_detail', 
			args=[str(article.pk)])
		)
	
	def test_only_author_can_edit_article(self):
		user1 = User.objects.create(username='testuser1', password='mypass123')
		user2 = User.objects.create(username='testuser2', password='mypass123')
		self.client.force_login(user1)
		response = self.client.post(reverse('article_new'), 
			data={ 'title': 'title', 'body': 'body', }
		)
		article = Article.objects.first()
		self.client.force_login(user2)
		response = self.client.post(reverse('article_edit', 
			args=[str(article.id)]), 
			data={ 'title': 'updated title', 'body': 'updated body', }
		)
		self.assertEqual(response.status_code, 403)
		
		

class ArticleDeleteViewTest(TestCase):
	
	def test_view_uses_right_template(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		response = self.client.get(reverse('article_delete', 
			args=[str(article.id)]))
		self.assertTemplateUsed(response, 'article_delete.html')			
	
	def test_view_redirects_back_to_detail_view_page(self):
		user = User.objects.create_user(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(
			title='article', body='first article', author=user
		)
		response = self.client.post(reverse('article_delete', 
			args=[str(article.id)]))
		self.assertRedirects(response, reverse('article_list'))
	
	def test_only_author_can_delete_article(self):
		user1 = User.objects.create(username='testuser1', password='mypass123')
		user2 = User.objects.create(username='testuser2', password='mypass123')
		self.client.force_login(user1)
		response = self.client.post(reverse('article_new'), 
			data={ 'title': 'title', 'body': 'body', }
		)
		article = Article.objects.first()
		self.client.force_login(user2)
		response = self.client.post(reverse('article_delete',
			args=[str(article.id)]
		))
		self.assertEqual(response.status_code, 403)
	
	
class ArticleCreateViewTest(TestCase):
	
	def test_view_uses_correct_template(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.get(reverse('article_new'))
		self.assertTemplateUsed(response, 'article_new.html')
	
	def test_article_is_created_by_post_request(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.post(reverse('article_new'), data={
			'title': 'title', 'body': 'body',
		})
		article = Article.objects.first()
		self.assertEqual(article.title, 'title')
		self.assertEqual(article.body, 'body')
		self.assertEqual(article.author, user)
	
	def test_redirects_to_list_page(self):
		user = User.objects.create()
		self.client.force_login(user)
		response = self.client.post(reverse('article_new'), data={
			'title': 'title', 'body': 'body',
		})
		article = Article.objects.first()
		self.assertRedirects(response, reverse('article_detail', 
			args=[str(article.id)]
		))
	def test_accessing_new_article_page_directly_redirects_back_to_login_page(self):
		response = self.client.get(reverse('article_new'))
		self.assertRedirects(response, '/users/login/?next=/articles/new/')
		

class CommentCreateViewTest(TestCase):
	
	def test_view_uses_correct_template(self):
		user = User.objects.create(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(title='title', body='body', author=user)
		response = self.client.get(reverse('add_comment',
			args=[str(article.id)]))
		self.assertTemplateUsed(response, 'add_comment.html')
		
	def test_can_add_comment_to_a_specific_article(self):
		user = User.objects.create(username='testuser', password='mypass123')
		self.client.force_login(user)
		article = Article.objects.create(title='title', body='body', author=user)
		self.client.post(reverse('add_comment',
			args=[str(article.id)]), data={'comment': 'first comment'})
		comment = Comment.objects.first()
		self.assertEqual(comment.article, article)
		
		
		

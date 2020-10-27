from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Article, Comment


class ArticleListView(LoginRequiredMixin, ListView):
	
	model = Article
	
	template_name = 'article_list.html'
	
	context_object_name = 'articles'
	
	login_url = 'login'


class ArticleDetailView(LoginRequiredMixin, DetailView):
	
	model = Article
	
	template_name = 'article_detail.html'
	
	context_object_name = 'article'
	
	login_url = 'login'


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
	
	model = Article
	
	template_name = 'article_edit.html'
	
	fields = ('title', 'body',)
	
	login_url = 'login'
	
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)
		

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
	
	model = Article
	
	template_name = 'article_delete.html'
	
	success_url = reverse_lazy('article_list')
	
	login_url = 'login'
	
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch( request, *args, **kwargs)
		
	
class ArticleCreateView(LoginRequiredMixin, CreateView):
	
	model = Article
	
	template_name = 'article_new.html'
	
	fields = ('title', 'body',)
	
	login_url = 'login'
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
	
	model = Comment
	
	template_name = 'add_comment.html'
	
	fields = ('comment',)
	
	login_url = 'login'
	
	context_object_name = 'comment'
	
	def form_valid(self, form):
		article = Article.objects.get(pk=self.kwargs['pk'])
		form.instance.article = article
		form.instance.author = self.request.user
		return super().form_valid(form)	
	

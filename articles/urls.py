from django.urls import path

from .views import (
	ArticleListView,
	ArticleUpdateView,
	ArticleDetailView,
	ArticleDeleteView, 
	ArticleCreateView,
	CommentCreateView,
)


urlpatterns = [
	path('new/', ArticleCreateView.as_view(), name='article_new'),
	path('', ArticleListView.as_view(), name='article_list'),
	
	path('<int:pk>/add_comment/',
		CommentCreateView.as_view(), name='add_comment'),
	
	path('<int:pk>/',
		ArticleDetailView.as_view(), name='article_detail'),
	
	path('<int:pk>/edit/',
		ArticleUpdateView.as_view(), name='article_edit'),
	
	path('<int:pk>/delete/',
		ArticleDeleteView.as_view(), name='article_delete'),
]

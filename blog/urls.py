from django.urls import path

from blog import views

urlpatterns = [
	path('', views.PostListView.as_view(), name='posts_list'),
	path('about/', views.AboutView.as_view(), name='about'),
	path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post/create/', views.CreatePostView.as_view(), name='create_post'),
	path('post/<int:post_id>/update/', views.UpdatePostView.as_view(), name='update_post'),
	path('post/<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete_post'),
	path('drafts/', views.DraftListView.as_view(), name='drafts_list')
]
from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
	# Post urls
	path('', views.PostListView.as_view(), name='list_posts'),
	path('post/create/', views.CreatePostView.as_view(), name='create_post'),
	path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post/<slug:slug>/publish/', views.publish_post, name='publish_post'),
	path('post/<slug:slug>/update/', views.UpdatePostView.as_view(), name='update_post'),
	path('post/<slug:slug>/delete/', views.DeletePostView.as_view(), name='delete_post'),
	path('drafts/', views.DraftListView.as_view(), name='drafts_list'),
	# Comment urls
	path('post/<slug:slug>/comment/', views.add_comments_to_post, name='add_comment'),
	path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
	path('comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
	path('comment/<int:comment_id>/delete/', views.remove_comment, name='remove_comment'),
	# Other
	path('about/', views.AboutView.as_view(), name='about'),
	path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
	# Password reset
	path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
]
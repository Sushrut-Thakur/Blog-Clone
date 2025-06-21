from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

from . import settings
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('blog.urls',  namespace='blog')),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('blog:list_posts')), name='logout'),
	path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
		template_name='registration/password_reset_done.html'
		), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
		template_name='registration/password_reset_confirm.html'
		), name='password_reset_confirm'),
	path('reset/complete', auth_views.PasswordResetCompleteView.as_view(
		template_name='registration/password_reset_complete.html'
	), name='password_reset_complete'),
]

if settings.DEBUG:
	from debug_toolbar.toolbar import debug_toolbar_urls
	urlpatterns += debug_toolbar_urls()

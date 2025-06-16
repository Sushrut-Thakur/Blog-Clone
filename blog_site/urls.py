from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('blog.urls',  namespace='blog')),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('blog:list_posts')), name='logout'),
]

if settings.DEBUG:
	from debug_toolbar.toolbar import debug_toolbar_urls
	urlpatterns += debug_toolbar_urls()

from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from blog.models import Post, Comment
from blog.forms import PostForm

# Create your views here.
class AboutView(TemplateView):
	template_name = 'about.html'

class PostListView(ListView):
	model = Post

	def get_queryset(self):
		return Post.objects.filter(
			published_date__lte=timezone.now()
		).order_by('-published_date')

class PostDetailView(DetailView):
	model = Post
	template_name = 'post_detail.html'

	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)


class CreatePostView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)
	
class DeletePostView(LoginRequiredMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('post_list')

	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)

class DraftListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_list.html'
	model = Post

	def get_queryset(self):
		return Post.objects.filter(
			published_date__isnull=True
		).order_by('created_date')
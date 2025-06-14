from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

##############################################
# POST VIEWS
##############################################

class AboutView(TemplateView):
	template_name = 'blog/about.html'

class PostListView(ListView):
	model = Post
	template_name = 'post_list.html'
	context_object_name = 'posts'

	def get_queryset(self):
		return Post.objects.filter(
			published_date__lte=timezone.now()
		).order_by('-published_date')

class PostDetailView(DetailView):
	model = Post
	template_name = 'post_detail.html'
	context_object_name = 'post'

	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)


class CreatePostView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	template_name = 'post_form.html'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

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
	template_name = 'post_delete.html'
	success_url = reverse_lazy('blog:posts_list')

	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)

class DraftListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_list.html'
	model = Post
	context_object_name = 'draft_posts'
	template_name = 'blog/post_draft_list.html'

	def get_queryset(self):
		return Post.objects.filter(
			published_date__isnull=True
		).order_by('created_date')
	
@login_required
def publish_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	post.publish()
	return redirect('blog:post_detail', post_id=post_id)

##############################################
# COMMENT VIEWS
##############################################

@login_required
def add_comments_to_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()

			return redirect('blog:post_detail', post_id=post.id)
	else:
		form = CommentForm()
	return render(request, 'blog/comment_form.html', {
		'form': form,
	})

@login_required
def approve_comment(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	comment.approve()
	return redirect('blog:post_detail', post_id=comment.post.id)

@login_required
def remove_comment(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	post_id = comment.post.id
	comment.delete()
	return redirect('blog:post_detail', post_id=post_id)
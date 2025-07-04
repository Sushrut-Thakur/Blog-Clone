from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.views.generic import (
	View,
	TemplateView,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	FormView,
)

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm, UserSignUpForm, UserPasswordResetForm
from blog.mixins import GetPostByIdMixin

##############################################
# POST VIEWS
##############################################

class AboutView(TemplateView):
	template_name = 'blog/about.html'

class PostListView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'posts'

	def get_queryset(self):
		return Post.objects.filter(
			published_date__lte=timezone.now()
		).order_by('-published_date')

class PostDetailView(GetPostByIdMixin, DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post = context['post']
		user = self.request.user

		visible_comments = []
		for comment in post.comments.all():
			if comment.approved:
				visible_comments.append(comment)
			elif user.is_authenticated:
				if user == post.author or user == comment.author or user.is_superuser:
					visible_comments.append(comment)

		context['visible_comments'] = visible_comments
		return context


class CreatePostView(LoginRequiredMixin, CreateView):
	template_name = 'blog/post_form.html'
	form_class = PostForm
	model = Post

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

class UpdatePostView(LoginRequiredMixin, GetPostByIdMixin, UpdateView):
	form_class = PostForm
	model = Post

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if self.request.user != obj.author and not self.request.user.is_superuser:
			messages.error(request, "You're not allowed to edit this post.")
			return redirect('blog:post_detail', slug=obj.slug)
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.object.slug})
	
class DeletePostView(LoginRequiredMixin, GetPostByIdMixin, DeleteView):
	model = Post
	template_name = 'blog/post_delete.html'
	success_url = reverse_lazy('blog:list_posts')

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if self.request.user != obj.author and not self.request.user.is_superuser:
			messages.error(request, "You're not allowed to delete this post.")
			return redirect('blog:post_detail', slug=obj.slug)
		return super().dispatch(request, *args, **kwargs)

class DraftListView(LoginRequiredMixin, ListView):
	model = Post
	context_object_name = 'draft_posts'
	template_name = 'blog/post_draft_list.html'

	def get_queryset(self):
		return Post.objects.filter(
			published_date__isnull=True,
			author=self.request.user
		).order_by('created_date')

class PublishPostView(LoginRequiredMixin, View):
	def get(self, request, slug, *args, **kwargs):
		post = get_object_or_404(Post, slug=slug)
		post.publish()
		messages.success(request, "Post published successfully.")
		return redirect('blog:post_detail', slug=slug)
		

##############################################
# COMMENT VIEWS
##############################################

class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blog/comment_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.post_obj = get_object_or_404(Post, slug=kwargs['slug'])
		return super().dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		form.instance.post = self.post_obj
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post'] = self.post_obj
		return context
	
	def get_success_url(self):
		return reverse('blog:post_detail', kwargs={
			'slug': self.post_obj.slug,
		})

class EditCommentView(LoginRequiredMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blog/comment_form.html'
	pk_url_kwarg = 'comment_id'

	def dispatch(self, request, *args, **kwargs):
		comment = self.get_object()
		if request.user != comment.author:
			messages.error(request, "You're not allowed to edit this comment.")
			return redirect('blog:post_detail', slug=comment.post.slug)
		return super().dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['edit_mode'] = True
		return context
	
	def get_success_url(self):
		return reverse('blog:post_detail', kwargs={
			'slug': self.object.post.slug,
		})
	
class ApproveCommentView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		comment = get_object_or_404(Comment, id=kwargs['comment_id'])
		if request.user != comment.post.author and not request.user.is_superuser:
			messages.error(request, "You don’t have permission to approve this comment.")
		else:
			comment.approve()
			messages.success(request, "Comment approved successfully.")
		return redirect('blog:post_detail', slug=comment.post.slug)

class RemoveCommentView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):
		comment = get_object_or_404(Comment, id=kwargs['comment_id'])
		slug = comment.post.slug
		if request.user != comment.author and request.user != comment.post.author and not request.user.is_superuser:
			messages.error(request, "You don’t have permission to remove this comment.")
		else:
			comment.delete()
			messages.success(request, "Comment deleted successfully.")
		return redirect('blog:post_detail', slug=slug)

##############################################
# DEFAULT VIEWS
##############################################

class SignUpView(FormView):
	template_name = 'registration/signup.html'
	form_class = UserSignUpForm
	success_url = reverse_lazy('blog:list_posts')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return super().form_valid(form)

class ResetPasswordView(PasswordResetView):
	form_class = UserPasswordResetForm
	template_name = 'registration/reset_password.html'
	success_url = reverse_lazy('password_reset_done')

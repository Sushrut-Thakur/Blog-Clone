from django.shortcuts import get_object_or_404
from blog.models import Post

class GetPostByIdMixin:
	def get_object(self, queryset=None):
		slug = self.kwargs.get('slug')
		return get_object_or_404(Post, slug=slug)
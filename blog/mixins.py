from django.shortcuts import get_object_or_404
from blog.models import Post

class GetPostByIdMixin:
	def get_object(self, queryset=None):
		post_id = self.kwargs.get('post_id')
		return get_object_or_404(Post, pk=post_id)
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	published_date = models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created_date']
		verbose_name = "Blog Post"
		verbose_name_plural = "Blog Posts"

	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def approved_comments(self):
		return self.comments.filter(approved=True)
	
	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'post_id': self.pk})
	
	def __str__(self):
		return self.title
	
class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

	def approve(self):
		self.approved = True
		self.save()

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={
			'post_id': self.post.id,
		})

	def __str__(self):
		return f"{self.author}: {self.text[:30]}..."

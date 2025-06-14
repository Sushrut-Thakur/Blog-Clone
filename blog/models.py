from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

CASCADE = models.CASCADE

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	published_date = models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=CASCADE)

	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def approved_comments(self):
		return self.comments.filter(approved=True)
	
	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'post_id': self.pk})
	
	def __str__(self):
		return self.title
	
class Comment(models.Model):
	author = models.CharField(max_length=200)
	text = models.TextField()
	approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Post, on_delete=CASCADE)

	def approve(self):
		self.approved = True
		self.save()

	def get_absolute_url(self):
		return reverse('post_list')

	def __str__(self):
		return self.text
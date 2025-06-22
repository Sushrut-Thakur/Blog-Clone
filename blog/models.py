from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(
		max_length=200,
		unique=True,
		help_text="Unique SEO-friendly URL generated from the title",
	)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	published_date = models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.title)
			slug = base_slug
			counter = 1
			while Post.objects.filter(slug=slug).exists():
				slug = f"{base_slug}-{counter}"
				counter += 1
			self.slug = slug

		super().save(*args, **kwargs)

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
		return reverse('blog:post_detail', kwargs={'slug': self.slug})
	
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
			'slug': self.post.slug,
		})

	def __str__(self):
		return f"{self.author}: {self.text[:30]}..."

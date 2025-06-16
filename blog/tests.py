from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post
from blog.forms import PostForm

# Create your tests here.
class PostTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user1', password='qwerty123')
		self.post = Post.objects.create(
			title="Blog Post 1",
			text="This is my first blog.",
			author=self.user,
			published_date=timezone.now()
		)
		self.draft = Post.objects.create(
			title="Blog Post 2",
			text="This is my second blog, but it's a draft.",
			author=self.user,
		)

	def test_post_model_str(self):
		self.assertEqual(str(self.post), "Blog Post 1")

	def test_index_shows_published_only(self):
		response = self.client.get(reverse('blog:list_posts'))
		self.assertContains(response, "Blog Post 1")

	def test_publish_post_sets_date(self):
		self.assertIsNone(self.draft.published_date)
		self.draft.publish()
		self.assertIsNotNone(self.draft.published_date)

	def test_post_detail_view(self):
		url = reverse('blog:post_detail', kwargs={
			'post_id': self.post.id,
		})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Blog Post 1")

	def test_create_post_requires_login(self):
		response = self.client.get(reverse('blog:create_post'))
		self.assertEqual(response.status_code, 302)

		self.client.login(username='user1', password='qwerty123')
		response = self.client.get(reverse('blog:create_post'))
		self.assertEqual(response.status_code, 200)

	def test_post_form_validation(self):
		invalid_data = PostForm(data={
			'title': '',
			'text': 'Missing title test',
		})
		self.assertFalse(invalid_data.is_valid())

		valid_data = PostForm(data={
			'title': 'Valid Blog',
			'text': 'No text missing',
		})
		self.assertTrue(valid_data.is_valid())
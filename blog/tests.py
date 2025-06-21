from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

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
			author=self.user
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

class CommentTests(TestCase):
	def setUp(self):
		self.post_author = User.objects.create_user(username='user1', password='qwerty123')
		self.comment_author = User.objects.create_user(username='user2', password='qwerty456')
		self.post = Post.objects.create(
			title="Blog Post 1",
			text="This is my first blog.",
			author=self.post_author,
			published_date=timezone.now()
		)
		self.comment1 = Comment.objects.create(
			post=self.post,
			author=self.comment_author,
			text='Loved the blog!!',
			approved=False
		)
		self.comment2 = Comment.objects.create(
			post=self.post,
			author=self.comment_author,
			text='Amazing writing!! I honestly could not stop reading. This comment needs to be more than 30 characters.',
			approved=False
		)

	def test_comment_model_str(self):
		self.assertEqual(str(self.comment1), f"{self.comment1.author}: {self.comment1.text[:30]}...")
		self.assertEqual(str(self.comment2), f"{self.comment2.author}: {self.comment2.text[:30]}...")

	def test_approve_function_works(self):
		self.assertFalse(self.comment1.approved)
		self.comment1.approve()
		self.assertTrue(self.comment1.approved)
	
	def test_post_approved_comments(self):
		self.comment1.approve()
		self.assertIn(self.comment1, self.post.approved_comments())
		self.assertNotIn(self.comment2, self.post.approved_comments())

	def test_add_comments_require_login(self):
		url = reverse('blog:add_comment', kwargs={'post_id': self.post.id})
		response = self.client.post(url, {'text': "Test comment"})
		self.assertEqual(response.status_code, 302)

		self.client.login(username='user2', password='qwerty456')
		response = self.client.post(url, {'text': "Test comment"}, follow=True)
		self.assertEqual(response.status_code, 200)
	
	def test_add_comment_successful(self):
		self.client.login(username='user2', password='qwerty456')
		url = reverse('blog:add_comment', kwargs={'post_id': self.post.id})
		response = self.client.post(url, {'text': "Test comment"}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Test comment")
	
	def test_only_author_edits_comments(self):
		url = reverse('blog:edit_comment', kwargs={'comment_id': self.comment1.id})

		self.client.login(username='user1', password='qwerty123')
		response = self.client.get(url, follow=True)
		self.assertContains(response, "not allowed")

		self.client.logout()
		self.client.login(username='user2', password='qwerty456')
		response = self.client.post(url, {'text': 'Edited Comment'}, follow=True)
		self.assertContains(response, "Edited Comment")

	def test_comment_form_validation(self):
		invalid_data = CommentForm(data={'text': ''})
		self.assertFalse(invalid_data.is_valid())

		valid = CommentForm(data={'text': 'Valid Comment'})
		self.assertTrue(valid.is_valid())

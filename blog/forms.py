from django import forms

from blog.models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text')
		labels = {
			'title': 'Blog Title',
			'text': 'Your Content',
		}
		help_texts = {
			'title': 'Use a catchy headline',
		}

		widgets = {
			'title': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Title of your post',
			}),
			'text': forms.Textarea(attrs={
				'class': 'editable medium-editor-textarea form-control',
				'rows': 10,
				'placeholder': 'Share your thoughts with the world...',
			})
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)

		widgets = {
			'text': forms.Textarea(attrs={
				'class': 'editable medium-editor-textarea'
			})
		}
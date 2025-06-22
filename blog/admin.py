from django.contrib import admin

from blog.models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	fields = ['author', 'title', 'text', 'published_date']
	search_fields = ['title']
	list_filter = ['published_date', 'author']
	list_display = ['title', 'slug', 'author']

class CommentAdmin(admin.ModelAdmin):
	fields = ['post', 'author', 'text', 'approved']
	list_display = ['comment', 'author', 'post', 'approved']
	list_editable = ['approved']

	def comment(self, obj):
		return (obj.text[:30] + '...') if len(obj.text) > 30 else obj.text

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

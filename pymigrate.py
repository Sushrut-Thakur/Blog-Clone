# populate_slugs.py

import os
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_site.settings')
django.setup()

from blog.models import Post

def populate_slugs():
    for post in Post.objects.all():
        if not post.slug:
            print("No slug")
        else:
            print(f"Slug = {post.slug}")
    print("✅ Done!")

if __name__ == '__main__':
    populate_slugs()

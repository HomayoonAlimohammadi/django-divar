from django.contrib import admin
from polls.models import Author, Post, Blog

admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Post)

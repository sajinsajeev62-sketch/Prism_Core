# blog/admin.py

from django.contrib import admin
from .models import Post, Comment, Bookmark, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'total_likes', 'total_comments']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'post__title']
    ordering = ['-created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'post__title']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
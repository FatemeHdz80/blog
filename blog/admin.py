from django.contrib import admin
from .models import Post, Comment



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'status', 'publish')
    list_filter = ['status']
    search_fields = ['title', 'body', 'author']
    date_hierarchy = 'publish'
    list_editable = ('status', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
from django.contrib import admin
from .models import Post, Tag, Comment, Subscribe


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscribe)
class CommentAdmin(admin.ModelAdmin):
    pass

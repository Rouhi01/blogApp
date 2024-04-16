from django.contrib import admin
from .models import Post, Tag, Comment, Subscribe, Profile, WebsiteMeta


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(WebsiteMeta)
class WebsiteMetaAdmin(admin.ModelAdmin):
    pass
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post, Tag


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        posts = Post.objects.all()
        context = {
            'posts':posts
        }
        return render(request, self.template_name, context)


class PostDetailView(View):
    template_name = 'home/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # Calculate the view count
        if post.view_count is None:
            post.view_count = 1
        else:
            post.view_count += 1
        post.save()

        context = {
            'post':post
        }
        return render(request, self.template_name, context)


class TagView(View):
    template_name = 'home/tag.html'

    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        context = {
            'posts':posts,
            'tag':tag
        }
        return render(request, self.template_name, context)


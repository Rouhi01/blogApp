from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        posts = Post.objects.all()
        context = {
            'posts':posts
        }
        return render(request, self.template_name)


class PostDetailView(View):
    template_name = 'home/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            'post':post
        }
        return render(request, self.template_name, context)


from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .models import Post, Tag, Comment
from .forms import CommentForm


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
    form_class = CommentForm

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm()

        # Calculate the view count
        if post.view_count is None:
            post.view_count = 1
        else:
            post.view_count += 1
        post.save()

        context = {
            'post':post,
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.post = post
            if request.user.is_authenticated:
                new_form.author = request.user
            new_form.save()
            return redirect(reverse('home:post_detail', kwargs={'slug':slug}))
        context = {
            'form':form,
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


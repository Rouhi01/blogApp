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

        # Get all comment of this post
        comments = Comment.objects.filter(post=post, is_reply=False)


        # Calculate the view count
        if post.view_count is None:
            post.view_count = 1
        else:
            post.view_count += 1
        post.save()

        context = {
            'post':post,
            'form':form,
            'comments':comments
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            parent = request.POST.get('parent')
            if parent:
                parent = Comment.objects.get(id=parent)
                if parent:
                    comment_reply = form.save(commit=False)
                    comment_reply.parent = parent
                    comment_reply.post = post
                    comment_reply.is_reply = True
                    if request.user.is_authenticated:
                        comment_reply.author = request.user
                    comment_reply.save()
                    return redirect(reverse('home:post_detail', kwargs={'slug':slug}))

            else:
                comment = form.save(commit=False)
                comment.post = post
                if request.user.is_authenticated:
                    comment.author = request.user
                comment.save()
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


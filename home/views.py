from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .models import Post, Tag, Comment, Profile
from .forms import CommentForm, SubscribeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count


class HomeView(View):
    template_name = 'home/home.html'
    form_class = SubscribeForm

    def setup(self, request, *args, **kwargs):
        posts = Post.objects.all()
        self.new_posts = posts.order_by('-updated_at')[0:3]
        self.top_posts = posts.order_by('-view_count')[0:3]
        featured_post = posts.filter(is_featured=True)
        if featured_post:
            self.featured_post = featured_post[0]
        super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            'new_posts':self.new_posts,
            'top_posts':self.top_posts,
            'featured_post':self.featured_post,
            'form':form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscribed Successfully')
            return redirect('home:home')

        context = {
            'new_posts':self.new_posts,
            'top_posts':self.top_posts,
            'featured_post': self.featured_post,
            'form':form
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


class AuthorView(View):
    template_name = 'home/author.html'

    def setup(self, request, *args, **kwargs):
        posts = Post.objects.all()
        self.profile = Profile.objects.get(slug=kwargs['slug'])
        self.new_posts = posts.filter(author=self.profile.user).order_by('-updated_at')[0:2]
        self.top_posts = posts.filter(author=self.profile.user).order_by('-view_count')[0:2]
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        top_authors = User.objects.annotate(number=Count('posts')).order_by('number')
        context = {
            'profile':self.profile,
            'top_posts':self.top_posts,
            'new_posts':self.new_posts,
            'top_authors':top_authors
        }
        return render(request, self.template_name, context)


class SearchView(View):
    template_name = 'home/search.html'
    def get(self, request):
        search_query = ''
        posts = None
        if request.GET.get('q'):
            search_query = request.GET.get('q')
            posts = Post.objects.filter(title__icontains=search_query)
        context = {
            'posts':posts,
            'search_query':search_query
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = 'home/about.html'
    def get(self, request):
        return render(request, self.template_name)


class AllPostView(View):
    template_name = 'home/all_post.html'

    def get(self, request):
        posts = Post.objects.all()

        context = {
            'posts':posts
        }
        return render(request, self.template_name, context)
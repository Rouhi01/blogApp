from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('Author/<slug:slug>/', views.AuthorView.as_view(), name='author'),
    path('search/', views.SearchView.as_view(), name='search'),
]

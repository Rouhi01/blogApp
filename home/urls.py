from django.urls import path
from . import views

app_name = 'home'
url_patterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

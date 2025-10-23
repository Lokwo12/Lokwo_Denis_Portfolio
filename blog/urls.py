from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('rss.xml', LatestPostsFeed(), name='post_feed'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from .models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Named URL patterns to include
        return [
            'portfolio:home',
            'portfolio:about',
            'portfolio:project_list',
            'portfolio:contact',
            'blog:post_list',
        ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.date

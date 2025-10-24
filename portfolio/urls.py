from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about.pdf', views.about_pdf, name='about_pdf'),
    path('sitemap/', views.html_sitemap, name='html_sitemap'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('gallery/', views.gallery, name='gallery'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('portfolio.pdf', views.portfolio_pdf, name='portfolio_pdf'),
]

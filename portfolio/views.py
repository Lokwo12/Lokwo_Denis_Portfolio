from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from blog.models import Post
from .models import Message, Project, Testimonial
from django.db import models
from .forms import ContactForm


def home(request):
	# simply render the homepage which contains the form
	posts = Post.objects.filter(published=True).order_by('-created_at')[:3]
	projects = Project.objects.order_by('-date')[:3]
	testimonials = Testimonial.objects.filter(featured=True)[:3]
	form = ContactForm()
	return render(request, 'home.html', {'posts': posts, 'projects': projects, 'testimonials': testimonials, 'form': form})


def contact(request):
	RATE_LIMIT_SECONDS = 30  # simple per-session rate limit
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			# basic rate limiting by session timestamp
			last = request.session.get('last_contact')
			now = timezone.now().timestamp()
			if last and (now - float(last) < RATE_LIMIT_SECONDS):
				messages.error(request, 'Please wait a moment before sending another message.')
				return redirect(reverse('portfolio:contact'))

			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			message_text = form.cleaned_data['message']

			# save to DB
			Message.objects.create(name=name, email=email, message=message_text)

			subject = f'Portfolio contact from {name}'
			body = f'From: {name} <{email}>\n\n{message_text}'
			recipient = getattr(settings, 'CONTACT_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
			try:
				send_mail(subject, body, None, [recipient], fail_silently=False)
			except Exception:
				# still show success but message remains in DB for inspection
				messages.warning(request, 'Received — but email delivery failed. Message saved.')
			else:
				messages.success(request, 'Thanks — your message was sent. I will get back to you soon.')

			request.session['last_contact'] = str(now)
			return redirect(reverse('portfolio:contact'))
	else:
		form = ContactForm()
	return render(request, 'contact.html', {'form': form})


def project_list(request):
    projects = Project.objects.all()
    tech = request.GET.get('tech')
    category = request.GET.get('category')
    search = request.GET.get('search')
    if tech:
        projects = projects.filter(technologies__icontains=tech)
    if category:
        projects = projects.filter(category__iexact=category)
    if search:
        projects = projects.filter(
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search) |
            models.Q(technologies__icontains=search)
        )
    categories = Project.objects.values_list('category', flat=True).distinct()
    techs = set()
    for p in Project.objects.all():
        techs.update(p.tech_list())
    return render(request, 'projects.html', {
        'projects': projects,
        'categories': categories,
        'techs': techs,
        'selected_tech': tech,
        'selected_category': category,
        'search': search,
    })


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from blog.models import Post
from .models import Message, Project, Testimonial, Tag
from django.db import models
from django.db.models import Count
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


def home(request):
	# simply render the homepage which contains the form
	posts = Post.objects.filter(published=True).order_by('-created_at')[:3]
	projects = Project.objects.order_by('-date')[:3]
	testimonials = Testimonial.objects.filter(featured=True)[:3]
	form = ContactForm()
	# Stats
	from django.utils import timezone as _tz
	current_year = _tz.now().year
	start_year = getattr(settings, 'CAREER_START_YEAR', current_year)
	years = max(1, current_year - int(start_year))
	projects_count = Project.objects.count()
	posts_count = Post.objects.filter(published=True).count()
	# Top technologies (tags)
	top_tags = list(Tag.objects.annotate(cnt=Count('projects')).order_by('-cnt', 'name')[:10].values_list('name', flat=True))
	featured_post = posts[0] if posts else None
	featured_project = Project.objects.order_by('-date').first()
	return render(request, 'home.html', {
		'posts': posts,
		'projects': projects,
		'testimonials': testimonials,
		'form': form,
		'stats': {
			'years': years,
			'projects': projects_count,
			'posts': posts_count,
		},
		'top_tags': top_tags,
		'featured_post': featured_post,
		'featured_project': featured_project,
	})


def about(request):
	"""Simple About page.
	Uses existing styles to present a bio, skills, and highlights.
	"""
	return render(request, 'about.html')


def contact(request):
	RATE_LIMIT_SECONDS = getattr(settings, 'CONTACT_RATE_LIMIT_SECONDS', 30)  # simple per-session rate limit
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
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
			msg_obj = Message.objects.create(
				name=name,
				email=email,
				message=message_text,
				attachment=form.cleaned_data.get('attachment')
			)

			subject = f'Portfolio contact from {name}'
			body = f'From: {name} <{email}>\n\n{message_text}'
			recipient = getattr(settings, 'CONTACT_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
			try:
				attachment = form.cleaned_data.get('attachment')
				if attachment:
					email_msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
					email_msg.attach(attachment.name, attachment.read(), getattr(attachment, 'content_type', None))
					email_msg.send(fail_silently=False)
				else:
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


def privacy(request):
	return render(request, 'privacy.html')


def terms(request):
	return render(request, 'terms.html')


def project_list(request):
	projects = Project.objects.all()
	tech = request.GET.get('tech')
	category = request.GET.get('category')
	search = request.GET.get('search')
	sort = request.GET.get('sort') or 'date_desc'
	per = request.GET.get('per') or '9'
	if tech:
		# Prefer normalized tags
		projects = projects.filter(models.Q(tags__name__iexact=tech) | models.Q(technologies__icontains=tech))
	if category:
		projects = projects.filter(category__iexact=category)
	if search:
		projects = projects.filter(
			models.Q(title__icontains=search) |
			models.Q(description__icontains=search) |
			models.Q(technologies__icontains=search)
		)
	# Sorting
	sort_map = {
		'date_desc': '-date',
		'date_asc': 'date',
		'title_asc': 'title',
		'title_desc': '-title',
	}
	projects = projects.order_by(sort_map.get(sort, '-date'))

	# Pagination
	try:
		per_int = int(per)
	except ValueError:
		per_int = 9
	if per_int not in (6, 9, 12, 24):
		per_int = 9
	paginator = Paginator(projects, per_int)
	page = request.GET.get('page') or 1
	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	categories = Project.objects.values_list('category', flat=True).exclude(category='').distinct()
	# Prefer normalized tags list
	techs = list(Tag.objects.values_list('name', flat=True))
	if not techs:
		# fallback to legacy split
		tech_set = set()
		for p in Project.objects.all():
			tech_set.update(p.tech_list())
		techs = sorted(tech_set)

	return render(request, 'projects.html', {
		'projects': page_obj.object_list,
		'page_obj': page_obj,
		'paginator': paginator,
		'categories': categories,
		'techs': techs,
		'selected_tech': tech,
		'selected_category': category,
		'search': search,
		'sort': sort,
		'per': per_int,
		'per_options': (6, 9, 12, 24),
		'has_filters': bool(tech or category or search),
	})


def portfolio_pdf(request):
	"""Generate a simple portfolio PDF with a project listing.
	If reportlab is not installed, return a helpful message.
	"""
	try:
		from reportlab.lib.pagesizes import A4
		from reportlab.pdfgen import canvas
		from reportlab.lib.units import mm
		from reportlab.lib.utils import simpleSplit
	except Exception as exc:
		return HttpResponse(
			"ReportLab is required to generate the PDF. Please install requirements and restart.",
			content_type='text/plain',
			status=500
		)

	# Prepare response
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Denis_Lokwo_Portfolio.pdf"'
	c = canvas.Canvas(response, pagesize=A4)
	width, height = A4

	# Margins
	margin_x = 20 * mm
	margin_y = 20 * mm
	y = height - margin_y

	# Title
	c.setFont("Helvetica-Bold", 18)
	c.drawString(margin_x, y, "Denis Lokwo — Portfolio")
	y -= 12 * mm

	# Intro
	c.setFont("Helvetica", 11)
	intro = (
		"Selected projects and highlights. For live demos and full details, visit the website."
	)
	for line in simpleSplit(intro, "Helvetica", 11, width - 2 * margin_x):
		c.drawString(margin_x, y, line)
		y -= 6 * mm

	y -= 4 * mm
	c.setFont("Helvetica-Bold", 14)
	c.drawString(margin_x, y, "Projects")
	y -= 8 * mm

	projects = Project.objects.order_by('-date')
	c.setFont("Helvetica", 11)
	for proj in projects:
		# Ensure there is space, else new page
		min_block = 18 * mm
		if y < margin_y + min_block:
			c.showPage()
			y = height - margin_y
			c.setFont("Helvetica", 11)

		# Title line
		title = f"{proj.title} — {proj.category or 'General'} ({proj.date:%b %Y})"
		for line in simpleSplit(title, "Helvetica", 11, width - 2 * margin_x):
			c.drawString(margin_x, y, line)
			y -= 6 * mm

		# Technologies
		tech = ", ".join(proj.tech_list())
		if tech:
			for line in simpleSplit(f"Tech: {tech}", "Helvetica", 10, width - 2 * margin_x):
				c.drawString(margin_x, y, line)
				y -= 5 * mm

		# Description (short)
		desc = (proj.description or "").strip()
		if desc:
			lines = simpleSplit(desc, "Helvetica", 10, width - 2 * margin_x)
			for line in lines[:5]:
				c.drawString(margin_x, y, line)
				y -= 5 * mm

		y -= 3 * mm

	# Footer note
	if y < margin_y + 12 * mm:
		c.showPage()
		y = height - margin_y
	c.setFont("Helvetica-Oblique", 9)
	site_url = request.build_absolute_uri('/')
	c.drawString(margin_x, margin_y, f"Generated from Denis Lokwo Portfolio — {site_url}")

	c.showPage()
	c.save()
	return response


def project_detail(request, slug: str):
	project = get_object_or_404(Project, slug=slug)
	# gather related projects via shared tags (optional small touch)
	related = Project.objects.exclude(pk=project.pk)
	if hasattr(project, 'tags') and project.tags.exists():
		related = related.filter(tags__in=project.tags.all()).distinct()[:3]
	else:
		related = related.order_by('-date')[:3]
	return render(request, 'project.html', {
		'project': project,
		'related': related,
	})


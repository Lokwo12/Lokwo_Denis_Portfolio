# Denis Lokwo — Portfolio (Django)

A professional portfolio and blog built with Django. It includes projects with case studies, blog posts, a polished contact page (with file uploads), testimonials, inline Calendly booking, a downloadable portfolio PDF, SEO metadata, sitemap/robots, and dark/light themes with accent variants.

## Features
- Projects: filters, sorting, pagination; normalized Tags; slug-based case studies; related projects
- Blog: list + detail, RSS feed (`/blog/rss.xml`)
- Contact: file upload with validation and email (attachments included)
- Calendly: inline embed with skeleton
- PDF export: `/portfolio.pdf` with ReportLab
- SEO: meta description, OpenGraph/Twitter, JSON-LD (Person, Breadcrumbs, Article), sitemap.xml, robots.txt
- Theming: dark/light + brand accents; animations
- Analytics: GA4 loaded only after consent; event tracking for CTAs, downloads, outbound links

## Requirements
- Python 3.11+
- Django 5.2+

## Local development

1. Create and activate a virtualenv.
2. Install requirements:

```powershell
pip install -r requirements.txt
```

3. Run migrations (and optionally create a superuser):

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Start the dev server:

```powershell
python manage.py runserver
```

## Environment variables (recommended)
- DEBUG=True | False
- ALLOWED_HOSTS=example.com,www.example.com
- CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
- DEFAULT_FROM_EMAIL=no-reply@example.com
- CONTACT_EMAIL=owner@example.com
- EMAIL_BACKEND (default console backend) or SMTP vars:
	- EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
- GA_MEASUREMENT_ID=G-XXXXXXX (enables analytics after consent)
- CALENDLY_URL=https://calendly.com/your-link (optional)
- CAREER_START_YEAR=2020

## Static files & production
- Static URL: `/static/`
- `WhiteNoise` is auto-enabled when `DEBUG=False`.
- On deploy, collect static files:

```powershell
python manage.py collectstatic --noinput
```

- Security toggles (set for HTTPS):
	- SECURE_SSL_REDIRECT=True
	- SESSION_COOKIE_SECURE=True
	- CSRF_COOKIE_SECURE=True
	- SECURE_HSTS_SECONDS=31536000

## Sitemaps & robots
- Sitemap: `/sitemap.xml` (static pages, blog posts, projects)
- Robots: `/robots.txt`

## Tests
```powershell
python manage.py test
```

## Notes
- Social images: default OG/Twitter image is `static/images/og-default.svg`. Project pages use the project image when available.
- To tweak the hero typing roles/speed, edit the `data-roles` and timing attributes in `portfolio/templates/home.html`.

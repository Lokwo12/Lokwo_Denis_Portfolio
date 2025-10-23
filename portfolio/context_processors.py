from django.conf import settings
from django.apps import apps

def analytics(request):
    return {
        'GA_MEASUREMENT_ID': getattr(settings, 'GA_MEASUREMENT_ID', None),
        'CALENDLY_URL': getattr(settings, 'CALENDLY_URL', ''),
    }

def profile(request):
    """Expose profile data to templates from settings.PROFILE with safe defaults."""
    profile = getattr(settings, 'PROFILE', {}) or {}
    # Try to load DB Profile if available
    try:
        Profile = apps.get_model('portfolio', 'Profile')
        # Prefer the profile with the most content (experience+education+cert+award), tie-break by updated_at
        db_obj = None
        profiles = list(Profile.objects.all())
        if profiles:
            def score(p):
                try:
                    return (
                        (getattr(p, 'experience_items').count() if hasattr(p, 'experience_items') else 0)
                        + (getattr(p, 'education_items').count() if hasattr(p, 'education_items') else 0)
                        + (getattr(p, 'certification_items').count() if hasattr(p, 'certification_items') else 0)
                        + (getattr(p, 'award_items').count() if hasattr(p, 'award_items') else 0),
                        p.updated_at
                    )
                except Exception:
                    return (0, getattr(p, 'updated_at', None))
            db_obj = sorted(profiles, key=score, reverse=True)[0]
    except Exception:
        db_obj = None
    if db_obj:
        # Build dict from model fields, preferring DB values when present
        db_data = {
            'name': db_obj.name,
            'title': db_obj.title,
            'summary': db_obj.summary,
            'location': db_obj.location,
            'email': db_obj.email,
            'phone': db_obj.phone,
            'whatsapp': db_obj.whatsapp,
            'skills': db_obj.skills or [],
            'tools': db_obj.tools or [],
            'languages': db_obj.languages or [],
            'interests': db_obj.interests or [],
            'links': db_obj.links or {},
            'experience': db_obj.experience or [],
            'education': db_obj.education or [],
            'certifications': db_obj.certifications or [],
            'awards': db_obj.awards or [],
            # Avatar URL (if set)
            'avatar_url': (db_obj.avatar.url if db_obj.avatar else None),
        }
        # Merge settings fallback for any missing fields
        for k, v in (profile or {}).items():
            db_data.setdefault(k, v)
        profile = db_data

        # If related items exist, override arrays with relational data for better admin UX
        using_db_related = False
        exp_count = edu_count = cert_count = award_count = 0
        try:
            exp_qs = getattr(db_obj, 'experience_items').all()
            if exp_qs.exists():
                using_db_related = True
                exp_count = exp_qs.count()
                profile['experience'] = [
                    {
                        'role': e.role,
                        'company': e.company,
                        'period': e.period,
                        'summary': e.summary,
                    } for e in exp_qs
                ]
            edu_qs = getattr(db_obj, 'education_items').all()
            if edu_qs.exists():
                using_db_related = True
                edu_count = edu_qs.count()
                profile['education'] = [
                    {
                        'degree': ed.degree,
                        'institution': ed.institution,
                        'period': ed.period,
                        'location': ed.location,
                        'gpa': ed.gpa,
                        'honors': ed.honors,
                        'summary': ed.summary,
                        'courses': (ed.courses or []),
                    } for ed in edu_qs
                ]
            cert_qs = getattr(db_obj, 'certification_items').all()
            if cert_qs.exists():
                using_db_related = True
                cert_count = cert_qs.count()
                # Templates expect a list of strings; format nicely
                certs = []
                for c in cert_qs:
                    parts = [c.name]
                    meta = ", ".join([p for p in [c.issuer, c.year] if p])
                    if meta:
                        parts.append(f"({meta})")
                    certs.append(" ".join(parts))
                profile['certifications'] = certs
            award_qs = getattr(db_obj, 'award_items').all()
            if award_qs.exists():
                using_db_related = True
                award_count = award_qs.count()
                awards = []
                for a in award_qs:
                    parts = [a.name]
                    meta = ", ".join([p for p in [a.issuer, a.year] if p])
                    if meta:
                        parts.append(f"({meta})")
                    awards.append(" ".join(parts))
                profile['awards'] = awards
        except Exception:
            pass
        # Debug info to help diagnose selection/rendering issues (only surfaced when DEBUG is true in template)
    profile['selected_profile_id'] = getattr(db_obj, 'id', None)
    profile['selected_profile_name'] = getattr(db_obj, 'name', None)
    profile['exp_count'] = exp_count
    profile['edu_count'] = edu_count
    profile['cert_count'] = cert_count
    profile['award_count'] = award_count
    profile['using_db_related'] = using_db_related
    # Normalize common list-like fields
    def as_list(value):
        if not value:
            return []
        if isinstance(value, (list, tuple)):
            return list(value)
        if isinstance(value, str):
            return [x.strip() for x in value.split(',') if x.strip()]
        return []

    profile.setdefault('name', 'Denis Lokwo')
    profile.setdefault('title', 'Full‑stack Developer — Django, React, TypeScript')
    profile.setdefault('summary', "I'm a full‑stack developer passionate about building fast, accessible, and elegant web applications. I enjoy solving hard problems, mentoring, and delivering production‑ready systems.")
    profile.setdefault('location', 'L’Aquila, Abruzzi, Italy')
    profile.setdefault('email', 'denis.lokwo@example.com')
    profile.setdefault('phone', '+39 123 456 7890')
    profile.setdefault('whatsapp', '+39 123 456 7890')
    # Derived fields
    import re
    profile['whatsapp_link'] = re.sub(r'[^0-9]', '', str(profile.get('whatsapp') or ''))
    profile['skills'] = as_list(profile.get('skills') or ['Python','Django','DRF','PostgreSQL','JavaScript','TypeScript','React','Tailwind','Docker','CI/CD'])
    profile['tools'] = as_list(profile.get('tools') or ['Git','Pytest','Poetry','Celery','Redis'])
    profile['languages'] = as_list(profile.get('languages') or ['English','Italian'])
    profile['interests'] = as_list(profile.get('interests') or ['Open Source','AI','Developer Experience'])
    profile.setdefault('links', {
        'linkedin': 'https://linkedin.com/in/denislokwo',
        'github': 'https://github.com/Lokwo12',
    })
    # Structured sections
    profile.setdefault('experience', [
        {'role':'Senior Full‑stack Developer','company':'Company Name','period':'2023 — Present','summary':'Leading delivery of scalable web apps, improving performance and developer productivity, mentoring juniors, and collaborating cross‑functionally.'},
        {'role':'Software Engineer','company':'Company Name','period':'2021 — 2023','summary':'Built APIs, dashboards, and automation for data‑heavy workflows. Focused on testing, typing, and reliable deploys.'},
    ])
    profile.setdefault('education', [
        {
            'degree':'BSc, Computer Science',
            'institution':'University of Example',
            'period':'2017 — 2021',
            'location':'L’Aquila, Italy',
            'gpa':'3.7/4.0',
            'honors':'Magna Cum Laude',
            'summary':'Strong foundation in algorithms, data structures, databases, and HCI.',
            'courses':['Algorithms','Operating Systems','Computer Networks','Databases','Human‑Computer Interaction']
        },
    ])
    profile['certifications'] = as_list(profile.get('certifications'))
    profile['awards'] = as_list(profile.get('awards'))

    # expose a debug flag so templates can conditionally reveal debugging aids
    profile['debug'] = getattr(settings, 'DEBUG', False)
    return {'PROFILE': profile}

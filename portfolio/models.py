from django.db import models
from django.urls import reverse


class Message(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    attachment = models.FileField(upload_to='messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} <{self.email}> on {self.created_at:%Y-%m-%d}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text="Comma-separated list of technologies", blank=True)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.URLField(blank=True)
    
    # New: normalized tags for stronger queries/admin
    # Keep the legacy 'technologies' field for backward compatibility and migration
    
    
    

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def tech_list(self):
        # Prefer normalized tags if available, else fallback to legacy comma-separated field
        if hasattr(self, 'tags') and self.tags.exists():
            return list(self.tags.values_list('name', flat=True))
        return [tech.strip() for tech in (self.technologies or '').split(',') if tech.strip()]

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', args=[self.slug])


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.role})"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Add the ManyToMany at end to avoid circular reference in editors
Project.add_to_class('tags', models.ManyToManyField('Tag', related_name='projects', blank=True))


class Profile(models.Model):
    """Editable profile content for About page and global use."""
    name = models.CharField(max_length=150, default='Denis Lokwo')
    title = models.CharField(max_length=220, blank=True)
    summary = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)

    # JSON content
    skills = models.JSONField(blank=True, null=True, help_text='List of skills')
    tools = models.JSONField(blank=True, null=True, help_text='List of tools/technologies')
    languages = models.JSONField(blank=True, null=True, help_text='List of languages')
    interests = models.JSONField(blank=True, null=True, help_text='List of interests')
    links = models.JSONField(blank=True, null=True, help_text='Dict of external links')
    experience = models.JSONField(blank=True, null=True, help_text='List of experience items')
    education = models.JSONField(blank=True, null=True, help_text='List of education items')
    certifications = models.JSONField(blank=True, null=True)
    awards = models.JSONField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Profile: {self.name}" 


class ExperienceItem(models.Model):
    profile = models.ForeignKey(Profile, related_name='experience_items', on_delete=models.CASCADE)
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    period = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.role} @ {self.company}" if self.company else self.role


class EducationItem(models.Model):
    profile = models.ForeignKey(Profile, related_name='education_items', on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    gpa = models.CharField(max_length=50, blank=True)
    honors = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    courses = models.JSONField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.degree} - {self.institution}" if self.institution else self.degree


class CertificationItem(models.Model):
    profile = models.ForeignKey(Profile, related_name='certification_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class AwardItem(models.Model):
    profile = models.ForeignKey(Profile, related_name='award_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

from django.db import models


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

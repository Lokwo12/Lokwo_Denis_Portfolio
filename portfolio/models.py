from django.db import models


class Message(models.Model):
	name = models.CharField(max_length=150)
	email = models.EmailField()
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	processed = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Message from {self.name} <{self.email}> on {self.created_at:%Y-%m-%d}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text="Comma-separated list of technologies")
    category = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


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

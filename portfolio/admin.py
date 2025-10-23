from django.contrib import admin
from .models import Message, Project, Testimonial
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse
from django import forms


class ReplyForm(forms.Form):
	subject = forms.CharField(max_length=200, initial='Re: Thanks for reaching out')
	body = forms.CharField(widget=forms.Textarea, initial='Thanks for contacting me. I will reply shortly.')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'created_at', 'processed')
	list_filter = ('processed', 'created_at')
	search_fields = ('name', 'email', 'message')
	readonly_fields = ('created_at',)
	actions = ['mark_processed']

	def get_urls(self):
		urls = super().get_urls()
		custom = [
			path('<int:message_id>/reply/', self.admin_site.admin_view(self.reply_view), name='portfolio_message_reply'),
		]
		return custom + urls

	def reply_view(self, request, message_id, *args, **kwargs):
		message = self.get_object(request, message_id)
		if request.method == 'POST':
			form = ReplyForm(request.POST)
			if form.is_valid():
				subject = form.cleaned_data['subject']
				body = form.cleaned_data['body']
				send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [message.email])
				message.processed = True
				message.save()
				self.message_user(request, 'Reply sent and message marked processed.')
				return redirect('..')
		else:
			form = ReplyForm()
		context = dict(self.admin_site.each_context(request), form=form, message=message)
		return TemplateResponse(request, 'admin/portfolio/reply.html', context)

	def mark_processed(self, request, queryset):
		updated = queryset.update(processed=True)
		self.message_user(request, f'{updated} message(s) marked processed')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    search_fields = ('title', 'description', 'technologies', 'category')
    list_filter = ('category', 'date')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'featured', 'created_at')
    search_fields = ('name', 'role', 'content')
    list_filter = ('featured', 'created_at')


from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'you@domain.com'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Tell me about your project',
        'rows': 6
    }))
    attachment = forms.FileField(required=False, help_text='Optional: attach a brief brief/spec (max 5MB, PDF or image)',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,image/*'}))
    # honeypot: should remain empty
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_hp(self):
        data = self.cleaned_data.get('hp')
        if data:
            raise forms.ValidationError('Spam detected')
        return data

    def clean_attachment(self):
        f = self.cleaned_data.get('attachment')
        if not f:
            return f
        max_mb = 5
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f'File too large (>{max_mb}MB)')
        valid_mimes = {'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/webp'}
        content_type = getattr(f, 'content_type', None)
        if content_type and content_type not in valid_mimes:
            raise forms.ValidationError('Unsupported file type. Please upload a PDF or image.')
        return f

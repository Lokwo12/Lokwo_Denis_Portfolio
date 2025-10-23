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
    # honeypot: should remain empty
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_hp(self):
        data = self.cleaned_data.get('hp')
        if data:
            raise forms.ValidationError('Spam detected')
        return data

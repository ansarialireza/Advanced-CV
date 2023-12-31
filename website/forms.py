from django import forms
from .models import Contact,Newsletter
from captcha.fields import CaptchaField

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'your-css-class'}),
            'budget': forms.NumberInput(attrs={'class': 'your-css-class'}),
            # Add other widgets as needed
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model=Newsletter
        fields='__all__'
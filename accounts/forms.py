# forms in account app
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User 

# class CustomPasswordResetForm(PasswordResetForm):
#     username = forms.CharField(max_length=150, required=True, help_text='Required. Your username.')

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise forms.ValidationError("This username does not exist.")
#         return username


class CustomPasswordResetForm(forms.Form):
    username_or_email = forms.CharField(max_length=150, required=True, help_text='Required. Your username or email')

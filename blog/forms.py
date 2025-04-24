from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Message')

class SignupForm(UserCreationForm):
    username = forms.CharField( 
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User name'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})  # بهتره برای ایمیل از EmailInput استفاده کنی
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password again'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

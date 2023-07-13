from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from mainpage.models import Image


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'my-input', 'style': 'color: blue;'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'my-input', 'style': 'color: blue;'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'my-input', 'style': 'color: blue;'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'my-input', 'style': 'color: blue;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'my-input', 'style': 'color: red;'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'my-input', 'style': 'color: red;'}))

class UploadPic(forms.ModelForm):
   class Meta:
        model = Image
        fields =['title','photo']
        widgets = { 'title': forms.TextInput(attrs={'style':'color:red'})}

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from pagedown.widgets import PagedownWidget

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': ('Username')}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('First Name')}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Last Name')}))
	email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'placeholder': ('Email')}))
	password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': ('Password')}))
	password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': ('Confirm Password')}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': ('Username')}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': ('Password')}))

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width')}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': ('full-width')}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': ('full-width')}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': ('full-width')}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
	image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': ('full-width')}))
	about = forms.CharField(widget=forms.Textarea(attrs={'class': ('message full-width')}))
	class Meta:
		model = Profile
		fields = ['image', 'about']
from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width'), 'placeholder': ('Enter post time')}))
	content = forms.CharField(required=True, widget=PagedownWidget())

	class Meta:
		model = Post
		fields = ['title', 'content',]
		
class UpdatePostForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width')}))
	content = forms.CharField(required=True, widget=PagedownWidget())

	class Meta:
		model = Post
		fields = ['title', 'content',]
#from .models import Comment
from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


# class CommentForm(forms.ModelForm):
# 	name	= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width'), 'placeholder': ('Enter your name.')}))
# 	email	= forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': ('full-width'), 'placeholder': ('Enter your email')}))
# 	body	= forms.CharField(required=True, widget=PagedownWidget())
# 	class Meta:
# 		model = Comment
# 		fields = ('name', 'email', 'body')
class PostForm(forms.ModelForm):
	title 	= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width'), 'placeholder': ('Enter post')}))
	body = forms.CharField(required=True, widget=PagedownWidget())
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model 	= Post
		fields 	= ['title', 'author', 'image', 'body', 'publish', 'status', 'tags',]

class UpdatePostForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width')}))
	body = forms.CharField(required=True, widget=PagedownWidget())
	image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': ('full-width')}))

	class Meta:
		model 	= Post
		fields 	= ['title', 'image', 'body', 'status', 'tags',]

class SearchForm(forms.Form):
    query = forms.CharField()
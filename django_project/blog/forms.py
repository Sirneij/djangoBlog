from .models import Comment
from django import forms
from .models import Post
from ckeditor_uploader.fields import RichTextUploadingField



class CommentForm(forms.ModelForm):
	body = RichTextUploadingField()
	class Meta:
		model = Comment
		fields = ('body',)
class PostForm(forms.ModelForm):
	title 	= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width'), 'placeholder': ('Enter post')}))
	body = RichTextUploadingField()
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model 	= Post
		fields 	= ['title', 'author', 'image', 'body', 'publish', 'status', 'tags',]

class UpdatePostForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': ('full-width')}))
	body = RichTextUploadingField()
	image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': ('full-width')}))

	class Meta:
		model 	= Post
		fields 	= ['title', 'image', 'body', 'status', 'tags',]

class SearchForm(forms.Form):
    query = forms.CharField()
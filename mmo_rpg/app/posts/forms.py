from django import forms
from .templatetags.categories_tag import categories_tag

class CommentForm(forms.Form):

    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': "comment-text",
        'placeholder': "Напишите свой комментарий, он будет виден всем после решения автора поста",
        'rows':"3"
    }))

class CreatePostForm(forms.Form):

    text = forms.CharField( widget=forms.Textarea(attrs={
        'class':'comment-text', 
        'name':"post-text", 
        'id':"post-text", 
        'required': True, 
        'placeholder': "Расскажите что нибудь"
    }))

    image1 = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'id':"file-upload-1"
    }))

    image2 = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'id':"file-upload-2"
    }))

    image3 = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'id':"file-upload-3"
    }))


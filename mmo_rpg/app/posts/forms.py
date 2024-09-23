from django import forms

class CommentForm(forms.Form):

    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': "comment-text",
        'placeholder': "Напишите свой комментарий, он будет виден всем после решения автора поста",
        'rows':"3"
    }))


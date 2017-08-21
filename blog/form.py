from django import forms
from django.forms import ModelForm, Textarea, TextInput
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'content']
        widgets = {
            'title': TextInput(attrs={'class': 'uk-width-1-1 uk-text-large'}),
            'summary': Textarea(attrs={'class': 'uk-width-1-1', 'rows': 3}),
            'content': Textarea(attrs={'id': 'content'}),
        }
        error_messages = {
            'content': {
                'required': "Content is required.",
            },
        }

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


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, min_length=8)
    password2 = forms.CharField(label="Confirm Password", max_length=100, min_length=8)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('password is wrong')

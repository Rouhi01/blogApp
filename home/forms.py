from django import forms
from .models import Comment, Subscribe


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name', 'email', 'content', 'website'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment....'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['website'].widget.attrs['placeholder'] = 'Website'


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

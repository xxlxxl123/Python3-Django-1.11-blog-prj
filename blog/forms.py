from django import forms

from .models import Article

class PostForm(forms.ModelForm):
        class Meta:
            model=Article
            fields=[
                'title',
                'content',
                'image',
                'draft',
                'publish'
            ]
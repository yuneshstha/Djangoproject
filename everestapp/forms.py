from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget


class NewsCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Write your comment...'
    }))
    commentername = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Name...'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your valid email...'
    }))


# class UploadFileForm(forms.Form):
#     file = forms.FileField()

class ClientNewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(),
            # 'content': forms.Textarea(attrs={
            #     'class': 'form-control summernote',
            # }),
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'class': 'form-control form-control-rounded',
                    'placeholder': 'Page Description',
                }
            }),
            'image': forms.ClearableFileInput(),
        }

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "username...",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter your password..."
    }))
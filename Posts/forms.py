from django import forms
from .models import Post, Role, Replies
from django_summernote.widgets import SummernoteWidget


class CreatePostForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        empty_label=None,
        queryset=Role.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'role',
            'text',
        ]
        widgets = {
            'text': SummernoteWidget(),
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = [
            'text',
        ]
        widgets = {
            'text': SummernoteWidget(),
        }

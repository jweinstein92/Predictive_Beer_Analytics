from django import forms
from app.models import*
from django.forms import ModelForm
from app.models import Comment

class CommentForm(forms.ModelForm):

    text = forms.CharField(label="Comment")
    class Meta:
        model = Comment
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
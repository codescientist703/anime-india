from django import forms
from .models import Reply, Topic, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['content']


class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control',
    }), max_length=6000)

    class Meta:
        model = Topic
        fields = ['title', 'category', 'content']
        category = forms.ModelChoiceField(
            queryset=Category.objects.all(), to_field_name="name")

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

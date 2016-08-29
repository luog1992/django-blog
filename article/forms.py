from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms
# Apply summernote to specific fields.


class BlogEditor(forms.Form):
    # instead of forms.Textarea
    title = forms.CharField(max_length=100, required=True)
    tags = forms.CharField()
    content = forms.CharField(widget=SummernoteInplaceWidget(
        attrs={'width': '100%', 'height': '800px'}), required=True)

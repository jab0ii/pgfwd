from django import forms
from django.utils.safestring import mark_safe

class AckForm(forms.Form):
    message = forms.CharField(label=mark_safe('Ack Message<br />'), 
                              widget=forms.Textarea)
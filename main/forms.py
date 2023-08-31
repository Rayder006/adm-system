from django import forms
from .models import Meta

class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['mes', 'valor']

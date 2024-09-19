# forms.py
from django import forms
from .models import Relationship

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ['name1', 'name2', 'relationship_start_date', 'relationship_start_time', 'message', 'youtube_link', 'photos']
        widgets = {
            'relationship_start_date': forms.DateInput(attrs={'type': 'date'}),
            'relationship_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

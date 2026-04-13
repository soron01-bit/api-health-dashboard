from django import forms

from .models import DataEntry


class DataEntryForm(forms.ModelForm):
    class Meta:
        model = DataEntry
        fields = ['date', 'title', 'category', 'value', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

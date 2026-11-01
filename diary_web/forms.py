"""
Forms for Personal Digital Diary.
Demonstrates OOP form design, DateTime input widgets, and validation.
"""

from datetime import date
from django import forms


class DiaryEntryForm(forms.Form):
    """
    Form for creating and updating daily diary entries with editorial styling.
    """
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control studio-input-title',
                'placeholder': 'Title of your day...',
                'autofocus': True,
                'id': 'journalTitleInput',
            }
        ),
        label="Entry Title",
    )
    
    entry_date = forms.DateField(
        required=True,
        initial=date.today,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control filter-input',
                'type': 'date',
                'id': 'journalDateInput',
            }
        ),
        label="Journal Date",
    )
    
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control studio-textarea',
                'rows': 12,
                'placeholder': 'What made today memorable? Write your raw thoughts, stories, highlights...',
                'id': 'journalContentArea',
            }
        ),
        label="Journal Content",
    )

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty or just spaces.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Journal content cannot be empty.")
        return content

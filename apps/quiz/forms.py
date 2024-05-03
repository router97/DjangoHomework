from django import forms

from .models import Completion


class CompletionForm(forms.ModelForm):
    class Meta:
        model = Completion
        fields = ('user', 'quiz', 'percentage', 'picked_answers')
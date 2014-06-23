from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        fields = ["question", "type", "required"]
        model = Question

    def clean_type(self):
        type = self.cleaned_data["type"]
        if self.instance and type != self.instance.type and self.instance.answers.exists():
            raise forms.ValidationError("Cannot change once this question has answers")
        return type

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


class BaseApplyForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, program, *args, **kwargs):
        self.program = program
        super(BaseApplyForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.program.applicants.filter(email=email).exists():
            raise forms.ValidationError("An application with that email address has already been submitted.")
        return email


class BulkLoadApplicantsForm(forms.Form):

    csv = forms.CharField(required=True, widget=forms.Textarea)

    def clean(self):
        # Ensure that no two mappings share the same column
        for name, value in self.cleaned_data.items():
            for name2, value2 in self.cleaned_data.items():
                if name != name2 and value and value == value2:
                    raise forms.ValidationError("You cannot choose the same source for more than one question.")

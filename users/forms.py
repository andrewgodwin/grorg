from __future__ import annotations

from django import forms

from grants.models import Program

from .models import User


class RegisterForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    program_code = forms.CharField(required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("User with this email already exists")
        return self.cleaned_data["email"]

    def clean_program_code(self):
        program = Program.objects.filter(
            join_code=self.cleaned_data["program_code"]
        ).first()
        if not program:
            raise forms.ValidationError("Invalid code")
        return program


class JoinForm(forms.Form):

    program_code = forms.CharField(required=True)

    def clean_program_code(self):
        program = Program.objects.filter(
            join_code=self.cleaned_data["program_code"]
        ).first()
        if not program:
            raise forms.ValidationError("Invalid code")
        return program

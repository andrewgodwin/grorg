import csv
import datetime
import collections
from django import forms
from django.db.transaction import atomic
from .program import ProgramView
from ..forms import BulkLoadApplicantsForm
from ..models import Applicant, Answer


class BulkLoadApplicants(ProgramView):
    """
    Allows bulk importing of applications using CSV.
    """

    time_formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    def get(self, request):
        return self.render("program-bulk-applicants.html", {
            "form": BulkLoadApplicantsForm(),
        })

    def post(self, request):
        # We always get a CSV file - parse it.
        reader = csv.reader([x.encode("utf8") for x in self.request.POST["csv"].split("\n")])
        rows = list(reader)
        headers = rows[0]
        column_choices = [("", "---")] + list(enumerate(headers))
        # Make form with question mapping fields
        fields = collections.OrderedDict([
            ("name", forms.ChoiceField(choices=column_choices, required=True)),
            ("email", forms.ChoiceField(choices=column_choices, required=True)),
            ("timestamp", forms.ChoiceField(choices=column_choices, required=False)),
        ])
        for question in self.program.questions.all():
            fields["q%s" % question.id] = forms.ChoiceField(choices=column_choices, required=True, label=question.question)
        form = type("BulkLoadMapForm", (BulkLoadApplicantsForm, ), fields)(request.POST)
        # Did they submit mappings for all questions? If not, show form
        if form.is_valid():
            # Save and import!
            errors = []
            successful = 0
            for i, row in enumerate(rows[1:]):
                try:
                    with atomic():
                        applicant = Applicant(
                            program = self.program,
                            name = row[int(form.cleaned_data["name"])],
                            email = row[int(form.cleaned_data["email"])],
                        )
                        if not applicant.name.strip():
                            raise ValueError("Name is blank")
                        if not applicant.email.strip():
                            raise ValueError("Email is blank")
                        if Applicant.objects.filter(program=self.program, email=applicant.email).exists():
                            raise ValueError("Email already exists")
                        # Parse datetime if present
                        if form.cleaned_data.get("timestamp", None):
                            for time_format in self.time_formats:
                                try:
                                    applicant.applied = datetime.datetime.strptime(row[int(form.cleaned_data["timestamp"])], time_format)
                                except ValueError:
                                    pass
                        applicant.save()
                        # Save answers
                        for key, offset in form.cleaned_data.items():
                            if key not in ["name", "email", "csv", "timestamp"]:
                                raw_answer = row[int(form.cleaned_data[key])]
                                question = self.program.questions.get(pk=key.lstrip("q"))
                                if question.type == "boolean":
                                    answer = str(not any((raw_answer.lower().strip() == no_word) for no_word in ("no", "false", "off", "", "0")))
                                elif question.type == "integer":
                                    if not raw_answer.strip():
                                        answer = None
                                    else:
                                        try:
                                            answer = str(int(raw_answer.strip()))
                                        except ValueError:
                                            raise ValueError("Invalid integer value for question %s: %s" % (question.question, raw_answer))
                                else:
                                    answer = raw_answer
                                Answer.objects.create(
                                    applicant = applicant,
                                    question = question,
                                    answer = answer,
                                )
                        successful += 1
                except Exception as e:
                    errors.append((i, row, e))
            return self.render("program-bulk-applicants-result.html", {
                "successful": successful,
                "errors": errors,
            })
        else:
            # Show mapping form
            return self.render("program-bulk-applicants.html", {
                "form": form,
            })

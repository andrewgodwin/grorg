import csv
import datetime
import collections
from django import forms
from django.db.transaction import atomic
from django.views.generic import TemplateView
from .program import ProgramMixin
from ..forms import BulkLoadUploadForm, BulkLoadMapBaseForm
from ..models import Applicant, Answer, UploadedCSV, Score


class BulkLoader(ProgramMixin):
    """
    Generic base class for bulk loaders.
    """

    def get_context_data(self):
        return {
            "form": BulkLoadUploadForm(),
        }

    def post(self, request):
        # If there's a CSV, load it into the database, otherwise retrieve
        # the one we stored there before.
        if "csv" in request.FILES:
            csv_obj = UploadedCSV.objects.create(csv=request.FILES["csv"].read())
        else:
            csv_obj = UploadedCSV.objects.get(pk=request.POST["csv_id"])
        # We always get a CSV file - parse it.
        reader = csv.reader([x for x in str(csv_obj.csv).split("\n")])
        rows = list(reader)
        headers = rows[0]
        column_choices = [("", "---")] + list(enumerate(headers))
        # Make form with question mapping fields
        fields = collections.OrderedDict(
            (name, forms.ChoiceField(choices=column_choices, required=required, label=label))
            for name, required, label in self.get_targets()
        )
        form_input = {"csv_id": csv_obj.pk}
        form_input.update(request.POST.items())
        form = type("BulkLoadMapForm", (BulkLoadMapBaseForm, ), fields)(form_input)
        # Did they submit mappings for all questions? If not, show form
        if form.is_valid():
            # Save and import!
            errors = []
            successful = 0
            target_map = dict(
                (name, int(value))
                for name, value in form.cleaned_data.items()
                if name != "csv_id" and value is not None
            )
            for i, row in enumerate(rows[1:]):
                try:
                    with atomic():
                        self.process_row(row, target_map)
                        successful += 1
                except Exception as e:
                    errors.append((i, row, e))
            csv_obj.delete()
            return self.render_to_response({
                "successful": successful,
                "errors": errors,
            })
        else:
            # Show mapping form
            return self.render_to_response({
                "form": form,
            })


class BulkLoadApplicants(BulkLoader, TemplateView):
    """
    Allows bulk importing of applications using CSV.
    """

    template_name = "program-bulk-applicants.html"

    time_formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    ]

    def get_targets(self):
        targets = [
            ("name", True, "Name"),
            ("email", True, "Email"),
            ("timestamp", False, "Timestamp"),
        ]
        for question in self.program.questions.all():
            targets.append((
                "q%s" % question.id,
                True,
                question.question,
            ))
        return targets

    def process_row(self, row, target_map):
        applicant = Applicant.objects.filter(program=self.program, email=row[target_map["email"]]).first()
        if not applicant:
            applicant = Applicant(
                program = self.program,
                name = row[target_map["name"]],
                email = row[target_map["email"]],
            )
        else:
            applicant.name = row[target_map["name"]]
        if not applicant.name.strip():
            raise ValueError("Name is blank")
        if not applicant.email.strip():
            raise ValueError("Email is blank")
        # Parse datetime if present
        if target_map.get("timestamp", None):
            for time_format in self.time_formats:
                try:
                    applicant.applied = datetime.datetime.strptime(row[target_map["timestamp"]], time_format)
                except ValueError:
                    pass
        applicant.save()
        # Save answers
        for key, offset in target_map.items():
            if key not in ["name", "email", "timestamp"]:
                raw_answer = row[target_map[key]]
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
                answer_obj = Answer.objects.filter(applicant=applicant, question=question).first()
                if not answer_obj:
                    answer_obj = Answer(
                        applicant = applicant,
                        question = question,
                    )
                answer_obj.answer = answer or ""
                answer_obj.save()


class BulkLoadScores(BulkLoader, TemplateView):
    """
    Allows bulk importing of scores using CSV.
    """

    template_name = "program-bulk-scores.html"


    def get_targets(self):
        return [
            ("email", True, "Email"),
            ("score", True, "Score"),
            ("comment", False, "Comment"),
        ]

    def process_row(self, row, target_map):
        applicant = Applicant.objects.get(email=row[target_map["email"]])

        score = Score.objects.get_or_create(applicant=applicant, user=self.request.user)[0]
        score_value = row[target_map["score"]]
        try:
            score.score = float(score_value)
        except ValueError:
            if not score_value.strip():
                raise ValueError("Score is blank")
            else:
                raise ValueError("Score is invalid: %s" % score_value)
        if "comment" in target_map:
            score.comment = row[target_map["comment"]]
        score.save()

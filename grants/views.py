import collections
from django import forms
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Program, Question, Answer, Applicant
from .forms import QuestionForm


def index(request):
    return render(request, "index.html", {
        "programs": Program.objects.order_by("name"),
    })


class ProgramView(View):
    """
    Generic view base class which does things in context of a Program.
    """

    def dispatch(self, *args, **kwargs):
        self.program_slug = kwargs.pop("program")
        self.program = Program.objects.get(slug=self.program_slug)
        return super(ProgramView, self).dispatch(*args, **kwargs)

    def render(self, template, context):
        context['program'] = self.program
        return render(self.request, template, context)


class ProgramHome(ProgramView):
    """
    Homepage for a Program.
    """

    def get(self, request):
        return self.render("program-home.html", {})


class ProgramQuestions(ProgramView):
    """
    Allows editing of questions on a Program.
    """

    def get(self, request):
        questions = self.program.questions.order_by("order")
        return self.render("program-questions.html", {
            "questions": questions,
            "form": QuestionForm(),
        })

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.program = self.program
            question.save()
            return redirect(".")
        else:
            return self.render("program-question-edit.html", {
                "form": form,
            })


class ProgramQuestionEdit(ProgramView):
    """
    Allows editing of a single question on a Program.
    """

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        form = QuestionForm(instance=question)
        return self.render("program-question-edit.html", {
            "form": form,
            "question": question,
        })

    def post(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        # Possible deletion?
        if "delete" in request.POST:
            question.delete()
            return redirect(self.program.urls.questions)
        # Save changes
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(self.program.urls.questions)
        else:
            return self.render("program-question-edit.html", {
                "form": form,
                "question": question,
            })


class ProgramApply(ProgramView):
    """
    Lets you apply for a program.
    """

    def get_form(self):
        fields = collections.OrderedDict([
            ("name", forms.CharField(required=True)),
            ("email", forms.EmailField(required=True)),
        ])
        for question in self.program.questions.order_by("order"):
            widget = forms.Textarea if question.type == "textarea" else None
            fields["question-%s" % question.id] = {
                "boolean": forms.BooleanField,
                "text": forms.CharField,
                "textarea": forms.CharField,
                "integer": forms.IntegerField,
            }[question.type](required=question.required, widget=widget, label=question.question)
        return type("ApplicationForm", (forms.Form, ), fields)

    def get(self, request):
        if request.method == "POST":
            form = self.get_form()(request.POST)
            if form.is_valid():
                applicant = Applicant.objects.create(
                    program = self.program,
                    name = form.cleaned_data["name"],
                    email = form.cleaned_data["email"],
                    applied = timezone.now(),
                )
                for question in self.program.questions.order_by("order"):
                    value = form.cleaned_data.get("question-%s" % question.id, None) or None
                    if value:
                        Answer.objects.create(
                            applicant = applicant,
                            question = question,
                            answer = value,
                        )
                return redirect(self.program.urls.apply_success)
        else:
            form = self.get_form()
        return self.render("program-apply.html", {
            "form": form,
        })

    post = get


class ProgramApplySuccess(ProgramView):
    """
    Shown after you've applied.
    """

    def get(self, request):
        return self.render("program-apply-success.html", {})


class ProgramApplications(ProgramView):
    """
    Shows applications to the program.
    """

    def get(self, request):
        applications = self.program.applicants.order_by("-applied")
        return self.render("program-applications.html", {
            "applications": applications,
        })


class ProgramApplicationView(ProgramView):
    """
    Shows an individual application.
    """

    def get(self, request, application_id):
        application = self.program.applicants.get(pk=application_id)
        questions = list(self.program.questions.order_by("order"))
        for question in questions:
            question.answer = question.answers.filter(applicant=application).first()
        return self.render("program-application-view.html", {
            "application": application,
            "questions": questions,
        })

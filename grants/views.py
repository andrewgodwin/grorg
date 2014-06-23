from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Program, Question
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
            self.render("program-question-edit.html", {
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

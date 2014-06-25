import collections
from django import forms
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, FormView, UpdateView
from ..models import Program, Question, Answer, Applicant, Score, Resource
from ..forms import QuestionForm, BaseApplyForm, ScoreForm, ResourceForm


def index(request):
    return render(request, "index.html", {
        "programs": Program.objects.order_by("name"),
    })


class ProgramMixin(object):
    """
    Generic view base class which does things in context of a Program.
    """

    login_required = True

    def dispatch(self, *args, **kwargs):
        self.program_slug = kwargs.pop("program")
        self.program = Program.objects.get(slug=self.program_slug)
        if self.login_required and not self.request.user:
            return redirect("login")
        return super(ProgramMixin, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **kwargs):
        context['program'] = self.program
        return super(ProgramMixin, self).render_to_response(context, **kwargs)


class ProgramHome(ProgramMixin, TemplateView):
    """
    Homepage for a Program.
    """

    template_name = "program-home.html"


class ProgramQuestions(ProgramMixin, FormView):
    """
    Allows editing of questions on a Program.
    """

    template_name = "program-questions.html"
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super(ProgramQuestions, self).get_context_data(**kwargs)
        context['questions'] = self.program.questions.order_by("order")
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        question.program = self.program
        question.save()
        return redirect(".")


class ProgramQuestionEdit(ProgramMixin, UpdateView):
    """
    Allows editing of a single question on a Program.
    """

    template_name = "program-question-edit.html"
    model = Question
    form_class = QuestionForm
    pk_url_kwarg = "question_id"

    def get_success_url(self):
        return self.program.urls.questions

    def post(self, request, question_id):
        # Possible deletion?
        if "delete" in request.POST:
            Question.objects.filter(pk=question_id).delete()
            return redirect(self.program.urls.questions)
        return UpdateView.post(self, request, question_id)


class ProgramApply(ProgramMixin, FormView):
    """
    Lets you apply for a program.
    """

    login_required = False
    template_name = "program-apply.html"

    def get_form_kwargs(self):
        kwargs = super(ProgramApply, self).get_form_kwargs()
        kwargs['program'] = self.program
        return kwargs

    def get_form_class(self):
        fields = collections.OrderedDict()
        for question in self.program.questions.order_by("order"):
            widget = forms.Textarea if question.type == "textarea" else None
            fields["question-%s" % question.id] = {
                "boolean": forms.BooleanField,
                "text": forms.CharField,
                "textarea": forms.CharField,
                "integer": forms.IntegerField,
            }[question.type](required=question.required, widget=widget, label=question.question)
        return type("ApplicationForm", (BaseApplyForm, ), fields)

    def form_valid(self, form):
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


class ProgramApplySuccess(ProgramMixin, TemplateView):
    """
    Shown after you've applied.
    """

    login_required = False
    template_name = "program-apply-success.html"


class ProgramApplicants(ProgramMixin, ListView):
    """
    Shows applications to the program.
    """

    template_name = "program-applicants.html"
    context_object_name = "applicants"

    def get_queryset(self):
        applicants = list(self.program.applicants.order_by("-applied"))
        for applicant in applicants:
            applicant.has_scored = applicant.scores.filter(user=self.request.user).exists()
        return applicants


class ProgramApplicantView(ProgramMixin, TemplateView):
    """
    Shows an individual application.
    """

    template_name = "program-applicant-view.html"

    def get(self, request, applicant_id):
        applicant = self.program.applicants.get(pk=applicant_id)
        questions = list(self.program.questions.order_by("order"))
        for question in questions:
            question.answer = question.answers.filter(applicant=applicant).first()
        # See if we already scored this one
        score = Score.objects.filter(applicant=applicant, user=self.request.user).first()
        old_score = score.score if score else None
        if score:
            all_scores = Score.objects.filter(applicant=applicant)
            form = ScoreForm(instance=score)
        else:
            all_scores = None
        if request.method == "POST":
            form = ScoreForm(request.POST, instance=score)
            if form.is_valid():
                new_score = form.save(commit=False)
                new_score.applicant = applicant
                new_score.user = self.request.user
                if old_score:
                    new_score.score_history = ",".join(
                        [x.strip() for x in (new_score.score_history or "").split(",") if x.strip()]
                        + ["%.1f" % old_score]
                    )
                new_score.save()
                return redirect(".")
        else:
            form = ScoreForm(instance=score)
        return self.render_to_response({
            "applicant": applicant,
            "questions": questions,
            "all_scores": all_scores,
            "form": form,
        })

    post = get


class ProgramResources(ProgramMixin, FormView):
    """
    Allows editing of resources available for a program.
    """

    form_class = ResourceForm
    template_name = "program-resources.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramResources, self).get_context_data(**kwargs)
        context['resources'] = self.program.resources.order_by("name")
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        question.program = self.program
        question.save()
        return redirect(".")


class ProgramResourceEdit(ProgramMixin, UpdateView):
    """
    Allows editing of a single resource on a Program.
    """

    template_name = "program-resource-edit.html"
    model = Resource
    form_class = ResourceForm
    pk_url_kwarg = "resource_id"

    def get_success_url(self):
        return self.program.urls.resources

    def post(self, request, resource_id):
        # Possible deletion?
        if "delete" in request.POST:
            Resource.objects.filter(pk=resource_id).delete()
            return redirect(self.program.urls.resources)
        return UpdateView.post(self, request, resource_id)

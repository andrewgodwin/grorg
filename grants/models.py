from __future__ import annotations

from django.db import models
from urlman import Urls


class Program(models.Model):
    """
    Something which is giving out grants - a workshop, a course,
    a conference, etc.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    applications_open = models.DateTimeField(blank=True, null=True)
    applications_close = models.DateTimeField(blank=True, null=True)
    grants_announced = models.DateTimeField(blank=True, null=True)
    program_starts = models.DateTimeField(blank=True, null=True)

    join_code = models.CharField(max_length=100, blank=True, null=True)

    completed = models.BooleanField(default=False)
    duplicate_emails = models.BooleanField(default=False)

    users = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return self.name

    class urls(Urls):
        view = "/{self.slug}/"
        questions = "{view}questions/"
        applicants = "{view}applicants/"
        applicants_bulk = "{view}applicants/bulk/"
        applicants_csv = "{view}applicants/csv/"
        scores_bulk = "{view}applicants/bulk_scores/"
        resources = "{view}resources/"
        users = "{view}users/"
        admin = "{view}admin/"
        apply = "{view}apply/"
        apply_success = "{view}apply/success/"
        score_random = "{view}applicants/random-unscored/"

    def user_allowed(self, user):
        return self.users.filter(pk=user.pk).exists()


class Resource(models.Model):
    """
    A resource that can be given out to grantees, be it a place, some
    money, free tickets, or so on. Always countable as integers.
    """

    TYPE_CHOICES = [
        ("money", "Money"),
        ("ticket", "Ticket"),
        ("place", "Place"),
        ("accomodation", "Accomodation"),
    ]

    program = models.ForeignKey(
        Program, related_name="resources", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    amount = models.PositiveIntegerField()

    class urls(Urls):
        edit = "{self.program.urls.resources}{self.id}/"

    def __str__(self):
        return self.name

    def fa_icon(self):
        return {
            "money": "money",
            "ticket": "ticket",
            "place": "user",
            "accomodation": "building-o",
        }.get(self.type, self.type)

    def amount_allocated(self):
        return sum(a.amount for a in self.allocations.all())

    def amount_remaining(self):
        return self.amount - self.amount_allocated()


class Question(models.Model):
    """
    A question asked of applicants.
    """

    TYPE_CHOICES = [
        ("boolean", "Yes/No"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("integer", "Integer value"),
    ]

    program = models.ForeignKey(
        Program, related_name="questions", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    question = models.TextField()
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class urls(Urls):
        edit = "{self.program.urls.questions}{self.id}/"

    def __str__(self):
        return self.question

    def can_delete(self):
        return not self.answers.exists()


class Applicant(models.Model):
    """
    Someone applying for a grant.
    """

    program = models.ForeignKey(
        Program, related_name="applicants", on_delete=models.CASCADE
    )
    name = models.TextField()
    email = models.EmailField()

    applied = models.DateTimeField(blank=True, null=True)

    class urls(Urls):
        view = "{self.program.urls.applicants}{self.id}/"
        allocations = "{view}allocations/"

    def __str__(self):
        return self.name

    def average_score(self):
        scores = [s.score for s in self.scores.all() if s.score]
        if not scores:
            return None
        else:
            return sum(scores) / float(len(scores))

    def variance(self):
        data = [s.score for s in self.scores.all() if s.score]
        n = len(data)
        if n == 0:
            return 0
        c = sum(data) / float(len(data))
        if n < 2:
            return 0
        ss = sum((x - c) ** 2 for x in data)
        ss -= sum((x - c) for x in data) ** 2 / len(data)
        assert not ss < 0, "negative sum of square deviations: %f" % ss
        return ss / (n - 1)

    def stdev(self):
        return self.variance() ** 0.5


class Allocation(models.Model):
    """
    An allocation of some Resources to an Applicant.
    """

    applicant = models.ForeignKey(
        Applicant, related_name="allocations", on_delete=models.CASCADE
    )
    resource = models.ForeignKey(
        Resource, related_name="allocations", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = [
            ("applicant", "resource"),
        ]


class Answer(models.Model):
    """
    An applicant's answer to a question.
    """

    applicant = models.ForeignKey(
        Applicant, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    answer = models.TextField()

    class Meta:
        unique_together = [
            ("applicant", "question"),
        ]


class Score(models.Model):
    """
    A score and optional comment on an applicant by a user.
    """

    applicant = models.ForeignKey(
        Applicant, related_name="scores", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="scores", on_delete=models.CASCADE
    )
    score = models.FloatField(
        blank=True, null=True, help_text="From 1 (terrible) to 5 (excellent)"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        help_text="Seen only by other voters, not by the applicant",
    )
    score_history = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [
            ("applicant", "user"),
        ]

    def score_history_human(self):
        return (self.score_history or "").replace(",", ", ")


class UploadedCSV(models.Model):
    """
    A place to store uploaded CSV files while they're being mapped.
    """

    csv = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)

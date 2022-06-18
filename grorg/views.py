from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    # -> https://adamj.eu/tech/2022/01/18/how-to-add-a-favicon-to-your-django-site/

    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + '<text y=".9em" font-size="90">🦄</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )

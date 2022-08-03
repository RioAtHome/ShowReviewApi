from django.urls import path, re_path
from django.views.generic.base import TemplateView
from .views import Routing

urlpatterns = [
    path(
        "docs",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    re_path(r"^", Routing.as_view()),
]

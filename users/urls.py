from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
]

from django.views import generic

from .models import Tutorial


class TutorialsListView(generic.ListView):
    context_object_name = 'tutorials'
    model = Tutorial
    template_name = "tutorials/tutorials.html"

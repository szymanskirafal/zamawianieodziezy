from django.urls import path

from . import views

app_name = "tutorials"
urlpatterns = [
    path(
        "",
        view=views.TutorialsListView.as_view(),
        name="tutorials",
    ),


]

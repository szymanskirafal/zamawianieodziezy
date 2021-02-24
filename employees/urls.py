from django.urls import path

from . import views

app_name = "employees"
urlpatterns = [
    path(
        "",
        view=views.EmployeesListView.as_view(),
        name="employees",
    ),
    path(
        "<int:pk>/",
        view=views.EmployeeDetailView.as_view(),
        name="employee",
    ),
    path(
        "add/",
        view=views.EmployeeCreateView.as_view(),
        name="add",
    ),
    path(
        "update/<int:pk>/",
        view=views.EmployeeUpdateView.as_view(),
        name="update",
    ),

]

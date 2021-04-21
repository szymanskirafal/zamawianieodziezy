from django.urls import path

from . import views

app_name = "supervisor"
urlpatterns = [
    path(
        "",
        view=views.SupervisorDashboardTemplateView.as_view(),
        name="dashboard",
    ),
    path(
        "order/<int:pk>",
        view=views.SupervisorOrderDetailView.as_view(),
        name="order",
    ),
    path(
        "order/<int:pk>/send/",
        view=views.SupervisorOrderUpdateView.as_view(),
        name="send",
    ),
    path(
        "order/sent/",
        view=views.SupervisorOrderSentTemplateView.as_view(),
        name="sent",
    ),
    path(
        "order/clothe/<int:pk>",
        view=views.SupervisorClotheDeleteView.as_view(),
        name="delete-clothe",
    ),


]

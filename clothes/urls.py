from django.urls import path

from . import views

app_name = "clothes"
urlpatterns = [
    path(
        "",
        view=views.KindsOfClothesListView.as_view(),
        name="kinds",
    ),
    path(
        "<int:kind_pk>/add-to-order/<int:employee_pk>/",
        view=views.ClotheCreateView.as_view(),
        name="clothe-create",
    ),
    path(
        "delete/<int:pk>/",
        view=views.ClotheDeleteView.as_view(),
        name="delete",
    ),
    path(
        "delivered/<int:pk>/",
        view=views.ClotheDeliveredUpdateView.as_view(),
        name="delivered",
    ),
    path(
        "delivered-with_defects/<int:pk>/",
        view=views.ClotheDeliveredWithDefectsUpdateView.as_view(),
        name="delivered_with_defects",
    ),
    path(
        "not-delivered/<int:pk>/",
        view=views.ClotheNotDeliveredUpdateView.as_view(),
        name="not_delivered",
    ),

]

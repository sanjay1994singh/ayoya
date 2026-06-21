from django.urls import path

from . import views

app_name = "properties"

urlpatterns = [
    path("", views.property_list, name="list"),
    path("create/", views.property_create, name="create"),
    path("category/<slug:slug>/", views.property_list, name="category"),
    path("<slug:slug>/", views.property_detail, name="detail"),
    path("<slug:slug>/edit/", views.property_edit, name="edit"),
    path("<slug:slug>/favorite/", views.toggle_favorite, name="favorite"),
]

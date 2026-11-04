from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="list"),
    path("new/", views.review_create, name="create"),
    path("<int:pk>/", views.review_detail, name="detail"),
    path("generate/", views.generation_list, name="generation_list"),
    path("generate/new/", views.generate_create, name="generate"),
    path("generate/<int:pk>/", views.generation_detail, name="generation_detail"),
]

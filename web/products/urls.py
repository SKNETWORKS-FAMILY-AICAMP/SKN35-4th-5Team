from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("new/", views.product_create, name="create"),
    path("<int:pk>/", views.product_detail, name="detail"),
    path("<int:pk>/edit/", views.product_update, name="update"),
    path("<int:pk>/delete/", views.product_delete, name="delete"),
    path("samples/<str:sample_id>/add/", views.sample_add, name="sample_add"),
]

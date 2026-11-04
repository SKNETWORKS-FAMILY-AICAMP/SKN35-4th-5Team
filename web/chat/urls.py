from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.session_list, name="list"),
    path("new/", views.session_create, name="create"),
    path("<int:pk>/", views.room, name="room"),
    path("<int:pk>/delete/", views.session_delete, name="delete"),
    path("<int:pk>/send/", views.send, name="send"),
]

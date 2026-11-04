from django.urls import path

from . import studio_views, views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # 3차 화면 중 빠져 있던 것 (core/studio_views.py)
    path("bulk/", studio_views.bulk, name="bulk"),
    path("library/", studio_views.library, name="library"),
    path("forecast/", studio_views.forecast, name="forecast"),
    path("health/", views.health, name="health"),
    path("health/ready/", views.ready, name="ready"),
]

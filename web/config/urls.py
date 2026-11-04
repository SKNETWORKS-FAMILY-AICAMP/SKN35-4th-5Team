from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("reviews/", include("reviews.urls")),
    path("chat/", include("chat.urls")),
    path("", include("core.urls")),
]

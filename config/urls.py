from django.contrib import admin
from django.urls import path, include
from drf_spectacular import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("lms/", include("lms.urls", namespace="lms")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("docs/schema/", views.SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/swagger/",
        views.SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "docs/redoc/",
        views.SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

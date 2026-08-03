from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from operations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/pnl/", views.pnl_report, name="pnl"),
    path("media/<path:path>", views.protected_media, name="protected_media"),
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

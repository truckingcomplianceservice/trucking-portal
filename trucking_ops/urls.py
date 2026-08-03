from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from operations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/pnl/", views.pnl_report, name="pnl"),
    path("reports/compliance/", views.compliance_report, name="compliance"),
    path("hiring/links/", views.hiring_links, name="hiring_links"),
    path("apply/done/", views.apply_thanks, name="apply_thanks"),
    path("apply/<str:token>/", views.apply_view, name="apply"),
    path("media/<path:path>", views.protected_media, name="protected_media"),
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

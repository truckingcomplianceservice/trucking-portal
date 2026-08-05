from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from operations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reports/", views.reports_index, name="reports"),
    path("reports/pnl/", views.pnl_report, name="pnl"),
    path("reports/tax/", views.tax_report, name="tax"),
    path("reports/factoring/", views.factoring_report, name="factoring"),
    path("reports/compliance/", views.compliance_report, name="compliance"),
    path("reports/activity/", views.activity_feed, name="activity"),
    path("tax/1099/<int:driver_id>/", views.generate_1099, name="generate_1099"),
    path("hiring/links/", views.hiring_links, name="hiring_links"),
    path("apply/done/", views.apply_thanks, name="apply_thanks"),
    path("apply/<str:token>/", views.apply_view, name="apply"),
    path("media/<path:path>", views.protected_media, name="protected_media"),
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

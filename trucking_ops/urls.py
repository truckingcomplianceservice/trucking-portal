from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from operations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", views.dashboard, name="dashboard"),
    # custom app sections
    path("app/loads/", views.app_loads, name="app_loads"),
    path("app/loads/<int:pk>/", views.app_load_detail, name="app_load_detail"),
    path("app/drivers/", views.app_drivers, name="app_drivers"),
    path("app/drivers/<int:pk>/", views.app_driver_detail, name="app_driver_detail"),
    path("app/vehicles/", views.app_vehicles, name="app_vehicles"),
    path("app/vehicles/<int:pk>/", views.app_vehicle_detail, name="app_vehicle_detail"),
    path("app/hiring/", views.app_hiring, name="app_hiring"),
    path("app/brokers/", views.app_brokers, name="app_brokers"),
    path("app/fuel/", views.app_fuel, name="app_fuel"),
    path("app/fuel/import/", views.fuel_import, name="fuel_import"),
    path("app/compliance/", views.app_compliance, name="app_compliance"),
    path("app/accounting/", views.app_accounting, name="app_accounting"),
    # reports
    path("reports/", views.reports_index, name="reports"),
    path("reports/builder/", views.report_builder, name="report_builder"),
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
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
]

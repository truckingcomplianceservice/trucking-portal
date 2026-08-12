from django.contrib.auth import views as auth_views
from django.views.static import serve as _serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from operations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("portfolio/", views.portfolio, name="portfolio"),
    # custom app sections
    path("app/loads/", views.app_loads, name="app_loads"),
    path("app/loads/from-ratecon/", views.load_from_ratecon, name="load_from_ratecon"),
    path("app/loads/<int:pk>/", views.app_load_detail, name="app_load_detail"),
    path("app/drivers/", views.app_drivers, name="app_drivers"),
    path("app/drivers/<int:pk>/", views.app_driver_detail, name="app_driver_detail"),
    path("app/drivers/<int:pk>/dqf/", views.app_driver_dqf, name="app_driver_dqf"),
    path("dqf/<int:doc_id>/approve/", views.dqf_approve, name="dqf_approve"),
    path("dqf/<int:doc_id>/reject/", views.dqf_reject, name="dqf_reject"),
    path("driver/<str:token>/", views.driver_upload, name="driver_upload"),

    path("app/vehicles/", views.app_vehicles, name="app_vehicles"),
    path("reports/maintenance/", views.fleet_maintenance, name="fleet_maintenance"),
    path("reports/maintenance/pdf/", views.fleet_maintenance_pdf, name="fleet_maintenance_pdf"),
    path("app/vehicles/<int:pk>/", views.app_vehicle_detail, name="app_vehicle_detail"),
    path("app/vehicles/<int:pk>/service/add/", views.maintenance_add, name="maintenance_add"),
    path("app/vehicles/<int:pk>/report/", views.vehicle_report_pdf, name="vehicle_report_pdf"),
    path("app/vehicles/<int:pk>/report/email/", views.email_vehicle_report, name="email_vehicle_report"),
    path("app/hiring/", views.app_hiring, name="app_hiring"),
    path("app/brokers/", views.app_brokers, name="app_brokers"),
    path("app/fuel/", views.app_fuel, name="app_fuel"),
    path("app/fuel/import/", views.fuel_import, name="fuel_import"),
    path("app/fuel/pdf/", views.fuel_report_pdf, name="fuel_report_pdf"),
    path("app/team/", views.app_team, name="app_team"),
    path("app/team/add/", views.team_add, name="team_add"),
    path("app/team/<int:pk>/toggle/", views.team_toggle_active, name="team_toggle_active"),
    path("app/team/<int:pk>/edit/", views.team_edit, name="team_edit"),
    path("app/team/<int:pk>/send-reset/", views.team_send_reset, name="team_send_reset"),
    path("app/timesheet/", views.app_timesheet, name="app_timesheet"),
    path("app/clock/", views.clock_toggle, name="clock_toggle"),

    path("app/compliance/", views.app_compliance, name="app_compliance"),
    path("app/accounting/", views.app_accounting, name="app_accounting"),
    path("app/billing/", views.app_billing, name="app_billing"),
    path("app/billing/new/", views.invoice_create, name="invoice_create"),
    path("app/billing/<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("app/billing/<int:pk>/pay/", views.payment_add, name="payment_add"),
    path("app/billing/<int:pk>/print/", views.invoice_print, name="invoice_print"),

    # reports
    path("reports/", views.reports_index, name="reports"),
    path("reports/builder/", views.report_builder, name="report_builder"),
    path("reports/pnl/", views.pnl_report, name="pnl"),
    path("reports/tax/", views.tax_report, name="tax"),
    path("reports/factoring/", views.factoring_report, name="factoring"),
    path("reports/factoring/aging/", views.factoring_aging, name="factoring_aging"),
    path("reports/factoring/aging/pdf/", views.factoring_aging_pdf, name="factoring_aging_pdf"),
    path("reports/compliance/", views.compliance_report, name="compliance"),
    path("reports/activity/", views.activity_feed, name="activity"),
    path("tax/1099/<int:driver_id>/", views.generate_1099, name="generate_1099"),
    path("tax/1099/<int:driver_id>/pdf/", views.generate_1099_pdf, name="generate_1099_pdf"),
    path("tax/1099/<int:driver_id>/email/", views.email_1099, name="email_1099"),
    path("hiring/links/", views.hiring_links, name="hiring_links"),
    path("apply/done/", views.apply_thanks, name="apply_thanks"),
    path("apply/<str:token>/", views.apply_view, name="apply"),
    path("media/<path:path>", views.protected_media, name="protected_media"),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
]

handler404 = "operations.views.go_home"

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", _serve, {"document_root": settings.MEDIA_ROOT}),
]

urlpatterns += [
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

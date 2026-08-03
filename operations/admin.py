"""
Admin configuration — the working interface for Phase 1.

Non-superusers only see data for the companies listed on their profile,
so a person from one company can't see another's drivers or loads.
"""
from django.contrib import admin
from .models import Company, Profile, Driver, Vehicle, Load

admin.site.site_header = "Trucking Operations Portal"
admin.site.site_title = "Trucking Portal"
admin.site.index_title = "Operations"


class CompanyScopedAdmin(admin.ModelAdmin):
    """Limit rows and company choices to the user's assigned companies."""
    company_field = "company"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed = request.user.profile.companies.all()
        return qs.filter(**{f"{self.company_field}__in": allowed})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.profile.companies.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "mc_number", "dot_number", "ca_number", "factor", "active")
    list_filter = ("factor", "active")
    search_fields = ("name", "mc_number", "dot_number", "ca_number")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk__in=request.user.profile.companies.all())


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)
    search_fields = ("user__username",)
    filter_horizontal = ("companies",)


@admin.register(Driver)
class DriverAdmin(CompanyScopedAdmin):
    list_display = ("first_name", "last_name", "company", "driver_type", "tax_status",
                    "cdl_class", "cdl_expiry", "medical_expiry", "status")
    list_filter = ("company", "driver_type", "tax_status", "status", "cdl_class")
    search_fields = ("first_name", "last_name", "cdl_number")
    fieldsets = (
        (None, {"fields": ("company", "user", ("first_name", "last_name"), ("phone", "email"), "status")}),
        ("License & medical", {"fields": ("cdl_number", "cdl_class", "cdl_expiry", "medical_expiry", "hire_date")}),
        ("Type & tax", {"fields": ("driver_type", "tax_status")}),
        ("Pay", {"fields": ("pay_type", "pay_rate", "notes")}),
    )


@admin.register(Vehicle)
class VehicleAdmin(CompanyScopedAdmin):
    list_display = ("unit_number", "company", "year", "make", "model", "plate",
                    "inspection_expiry", "status")
    list_filter = ("company", "status")
    search_fields = ("unit_number", "vin", "plate")


@admin.register(Load)
class LoadAdmin(CompanyScopedAdmin):
    list_display = ("reference", "company", "customer", "origin", "destination",
                    "pickup_date", "rate", "miles", "status", "payment_status", "driver")
    list_filter = ("company", "status", "payment_status")
    search_fields = ("reference", "customer", "origin", "destination")
    date_hierarchy = "pickup_date"
    autocomplete_fields = ()

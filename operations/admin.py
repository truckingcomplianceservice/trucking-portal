"""
Admin configuration — the working interface for Phase 1.

Non-superusers only see data for the companies listed on their profile,
so a person from one company can't see another's drivers or loads.
"""
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (VehiclePhoto, ApplicantStatusHistory, Company, Profile, Driver, Vehicle, Load, Expense,
                     Settlement, Applicant, ComplianceDocument, ActivityLog, NotificationRule,
                     Broker, BrokerAgent, FuelTransaction, TimeEntry, Invoice, Payment, MaintenanceRecord,
                     RentalContract, VehicleDocument, CompanyDocument)


class RentalContractInline(admin.TabularInline):
    model = RentalContract
    extra = 0
    fields = ("lessor", "start_date", "end_date", "base_amount", "base_period", "per_mile_rate", "active")

class VehicleDocumentInline(admin.TabularInline):
    model = VehicleDocument
    extra = 0
    fields = ("doc_type", "title", "file", "expiry_date")


class CategoryTextInput(forms.TextInput):
    """A text box with a dropdown of common categories (still lets you type anything)."""
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs["list"] = "expense-categories"
        html = super().render(name, value, attrs, renderer)
        options = "".join(f'<option value="{c}">' for c in Expense.COMMON_CATEGORIES)
        return mark_safe(f'{html}<datalist id="expense-categories">{options}</datalist>')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        widgets = {"category": CategoryTextInput()}

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
    readonly_fields = ("application_link",)

    @admin.display(description="Driver application link")
    def application_link(self, obj):
        if not obj.apply_token:
            return "(save first to generate)"
        return mark_safe(f'<code>/apply/{obj.apply_token}/</code> '
                         f'&mdash; add your domain in front. See Hiring &rarr; links page.')

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
    inlines = [RentalContractInline, VehicleDocumentInline]
    list_display = ("unit_number", "company", "year", "make", "model", "plate",
                    "inspection_expiry", "status")
    list_filter = ("company", "status")
    search_fields = ("unit_number", "vin", "plate")


@admin.register(Load)
class LoadAdmin(CompanyScopedAdmin):
    list_display = ("reference", "company", "customer", "origin", "destination",
                    "pickup_date", "rate", "miles", "deadhead_miles", "status", "payment_status", "driver")
    list_filter = ("company", "status", "payment_status")
    search_fields = ("reference", "customer", "origin", "destination")
    date_hierarchy = "pickup_date"
    fieldsets = (
        (None, {"fields": ("company", "reference", "customer", ("origin", "destination"),
                           ("pickup_date", "delivery_date"), ("rate", "miles", "deadhead_miles"),
                           ("driver", "vehicle"), ("status", "payment_status"), "notes")}),
        ("Documents & billing", {"fields": ("invoice_number", "bill_of_lading",
                           "proof_of_delivery", "rate_confirmation")}),
    )


@admin.register(Expense)
class ExpenseAdmin(CompanyScopedAdmin):
    form = ExpenseForm
    list_display = ("date", "company", "category", "amount", "vendor", "driver", "vehicle", "load")
    list_filter = ("company", "category")
    search_fields = ("vendor", "notes", "category")
    date_hierarchy = "date"


@admin.register(Settlement)
class SettlementAdmin(CompanyScopedAdmin):
    list_display = ("driver", "company", "period_start", "period_end",
                    "gross_pay", "deductions", "net_pay_display")
    list_filter = ("company", "driver")
    date_hierarchy = "period_end"

    @admin.display(description="Net pay")
    def net_pay_display(self, obj):
        return f"${obj.net_pay:,.2f}"


@admin.register(Applicant)
class ApplicantAdmin(CompanyScopedAdmin):
    list_display = ("first_name", "last_name", "company", "stage", "phone",
                    "cdl_class", "created_at")
    list_filter = ("company", "stage")
    search_fields = ("first_name", "last_name", "phone", "email")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    actions = ["hire_selected", "decline_selected"]

    @admin.action(description="Hire selected applicants (create driver + DQ file)")
    def hire_selected(self, request, queryset):
        created = 0
        for a in queryset.exclude(stage="cleared"):
            driver = Driver.objects.create(
                company=a.company, first_name=a.first_name, last_name=a.last_name,
                phone=a.phone, email=a.email, cdl_number=a.cdl_number,
                cdl_class=a.cdl_class or "", status="active",
                driver_type="company", tax_status="w2",
            )
            ComplianceDocument.objects.create(
                company=a.company, driver=driver, doc_type="application",
                issued_date=a.created_at.date(), verified=False,
                notes="Created from online application.")
            a.stage = "cleared"; a.save()
            created += 1
        self.message_user(request, f"Hired {created} applicant(s) and created their driver records.")

    @admin.action(description="Decline selected applicants")
    def decline_selected(self, request, queryset):
        n = queryset.update(stage="declined")
        self.message_user(request, f"Declined {n} applicant(s).")


@admin.register(ComplianceDocument)
class ComplianceDocumentAdmin(CompanyScopedAdmin):
    list_display = ("driver", "company", "doc_type", "issued_date", "expiry_date", "verified")
    list_filter = ("company", "doc_type", "verified")
    search_fields = ("driver__first_name", "driver__last_name")
    date_hierarchy = "expiry_date"


@admin.register(NotificationRule)
class NotificationRuleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "in_app", "email", "sms")
    list_editable = ("in_app", "email", "sms")

    def has_add_permission(self, request):
        return False  # rules are seeded; you just toggle them

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "company", "category", "text")
    list_filter = ("company", "category")
    search_fields = ("text",)
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False


class BrokerAgentInline(admin.TabularInline):
    model = BrokerAgent
    extra = 1


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ("name", "mc_number", "phone", "city", "state", "email")
    search_fields = ("name", "mc_number", "city")
    inlines = [BrokerAgentInline]


@admin.register(BrokerAgent)
class BrokerAgentAdmin(admin.ModelAdmin):
    list_display = ("name", "broker", "phone", "extension", "email")
    search_fields = ("name", "broker__name")
    list_filter = ("broker",)


@admin.register(FuelTransaction)
class FuelTransactionAdmin(CompanyScopedAdmin):
    list_display = ("date", "company", "vehicle", "driver", "location", "gallons", "amount", "receipt", "source")
    list_filter = ("company", "source")
    search_fields = ("location", "card_last4")
    date_hierarchy = "date"


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "clock_in", "clock_out", "hours")
    list_filter = ("user",)
    date_hierarchy = "clock_in"


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(CompanyScopedAdmin):
    list_display = ("invoice_number", "company", "bill_to", "issue_date", "due_date", "total", "balance", "status")
    list_filter = ("company",)
    search_fields = ("invoice_number", "bill_to_name")
    date_hierarchy = "issue_date"
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "payment_date", "transaction_id")
    list_filter = ("method",)
    date_hierarchy = "payment_date"


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(CompanyScopedAdmin):
    list_display = ("vehicle", "date", "part", "parts_cost", "labor_cost", "total", "receipt")
    list_filter = ("company", "vehicle")
    search_fields = ("part", "vendor")
    date_hierarchy = "date"


from .models import Task, PerformanceNote

@admin.register(Task)
class TaskAdmin(CompanyScopedAdmin):
    list_display = ("title", "company", "assignee", "driver", "vehicle", "priority", "status", "due_date")
    list_filter = ("status", "priority", "company")
    search_fields = ("title", "details")

@admin.register(PerformanceNote)
class PerformanceNoteAdmin(CompanyScopedAdmin):
    list_display = ("date", "company", "driver", "vehicle", "member", "rating")
    list_filter = ("company", "rating")


from .models import TeamNote

@admin.register(TeamNote)
class TeamNoteAdmin(CompanyScopedAdmin):
    list_display = ("created_at", "company", "author", "subject_label", "pinned")
    list_filter = ("company", "pinned")
    search_fields = ("body",)


@admin.register(RentalContract)
class RentalContractAdmin(CompanyScopedAdmin):
    list_display = ("vehicle", "lessor", "start_date", "end_date", "base_amount", "base_period", "per_mile_rate", "active")
    list_filter = ("company", "active", "base_period")
    search_fields = ("lessor",)


@admin.register(VehicleDocument)
class VehicleDocumentAdmin(CompanyScopedAdmin):
    list_display = ("vehicle", "doc_type", "title", "expiry_date", "uploaded_at")
    list_filter = ("company", "doc_type")


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(CompanyScopedAdmin):
    list_display = ("company", "doc_type", "title", "expiry_date", "uploaded_at")
    list_filter = ("company", "doc_type")


@admin.register(ApplicantStatusHistory)
class ApplicantStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("applicant", "from_stage", "to_stage", "changed_by", "changed_at")
    list_filter = ("to_stage",)


@admin.register(VehiclePhoto)
class VehiclePhotoAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "caption", "uploaded_at")

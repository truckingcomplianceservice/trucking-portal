"""
Phase 1 data model: the foundation of the trucking portal.

Companies (each with its own MC/DOT/CA and factor), Drivers, Vehicles,
Loads, and user Profiles that control role and which companies a person
can access.
"""
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    FACTOR_CHOICES = [
        ("RTS", "RTS Financial"),
        ("Bobtail", "Bobtail"),
        ("Other", "Other"),
        ("None", "No factoring"),
    ]
    name = models.CharField(max_length=120)
    mc_number = models.CharField("MC number", max_length=30, blank=True)
    dot_number = models.CharField("DOT number", max_length=30, blank=True)
    ca_number = models.CharField("CA number", max_length=30, blank=True)
    ein = models.CharField("EIN (federal tax ID)", max_length=20, blank=True)
    address = models.CharField("Mailing address", max_length=250, blank=True)
    factor = models.CharField(max_length=10, choices=FACTOR_CHOICES, default="None")
    active = models.BooleanField(default=True)
    apply_token = models.CharField(max_length=32, blank=True, db_index=True,
        help_text="Used to build this company's public driver-application link.")

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.apply_token:
            self.apply_token = secrets.token_urlsafe(12)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("dispatcher", "Dispatcher"),
        ("compliance", "Compliance manager"),
        ("safety", "Safety officer"),
        ("accountant", "Accountant"),
        ("billing", "Billing"),
        ("driver", "Driver"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="dispatcher")
    phone = models.CharField(max_length=30, blank=True)
    companies = models.ManyToManyField(
        Company, blank=True,
        help_text="Which companies this person can access. Leave empty for none.",
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Driver(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    CDL_CLASS_CHOICES = [("A", "Class A"), ("B", "Class B"), ("C", "Class C")]
    TYPE_CHOICES = [("company", "Company driver"), ("owner_operator", "Owner-operator")]
    TAX_CHOICES = [("w2", "W-2 employee"), ("1099", "1099 contractor")]
    PAY_TYPE_CHOICES = [
        ("per_mile", "Per mile"),
        ("percentage", "Percentage of load"),
        ("salary", "Salary"),
    ]

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="drivers")
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Optional login so the driver can see their own loads and pay.",
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    cdl_number = models.CharField("CDL number", max_length=40, blank=True)
    cdl_class = models.CharField("CDL class", max_length=1, choices=CDL_CLASS_CHOICES, blank=True)
    cdl_expiry = models.DateField("CDL expiry", null=True, blank=True)
    medical_expiry = models.DateField("Medical card expiry", null=True, blank=True)

    hire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    driver_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default="company",
        help_text="Owner-operators can see load rates; company drivers see miles only.")
    tax_status = models.CharField(max_length=5, choices=TAX_CHOICES, default="w2",
        help_text="1099 contractors get a 1099-NEC; W-2 employees go through payroll.")

    pay_type = models.CharField(max_length=12, choices=PAY_TYPE_CHOICES, default="per_mile")
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        help_text="Cents per mile, percent (e.g. 25), or weekly salary amount.")
    tax_id = models.CharField("Tax ID (SSN/EIN, for 1099)", max_length=20, blank=True)
    address = models.CharField("Mailing address", max_length=250, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("shop", "In shop"), ("inactive", "Inactive")]

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="vehicles")
    unit_number = models.CharField(max_length=30)
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    vin = models.CharField("VIN", max_length=30, blank=True)
    plate = models.CharField(max_length=20, blank=True)
    inspection_expiry = models.DateField("Annual inspection expiry", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    class Meta:
        ordering = ["unit_number"]

    def __str__(self):
        return f"Unit {self.unit_number}"


class Load(models.Model):
    STATUS_CHOICES = [
        ("booked", "Booked"), ("dispatched", "Dispatched"), ("in_transit", "In transit"),
        ("delivered", "Delivered"), ("invoiced", "Invoiced"), ("paid", "Paid"),
    ]
    PAYMENT_CHOICES = [
        ("unpaid", "Unpaid"), ("submitted", "Submitted to factor"),
        ("advanced", "Advanced"), ("reserve_released", "Reserve released"), ("closed", "Closed"),
    ]

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="loads")
    reference = models.CharField("Load / reference #", max_length=40)
    customer = models.CharField("Broker / customer", max_length=120, blank=True)
    broker = models.ForeignKey("Broker", on_delete=models.SET_NULL, null=True, blank=True, related_name="loads")
    origin = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    pickup_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miles = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="booked")
    payment_status = models.CharField(max_length=18, choices=PAYMENT_CHOICES, default="unpaid")
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=40, blank=True)
    bill_of_lading = models.FileField("Bill of Lading (BOL)", upload_to="loads/bol/", blank=True)
    proof_of_delivery = models.FileField("Proof of Delivery (POD)", upload_to="loads/pod/", blank=True)
    rate_confirmation = models.FileField(upload_to="loads/ratecon/", blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-pickup_date"]

    def __str__(self):
        return f"Load {self.reference}: {self.origin} -> {self.destination}"


class Expense(models.Model):
    # Common categories offered as suggestions, but you can type any category.
    COMMON_CATEGORIES = [
        "Fuel", "Maintenance / repair", "Insurance", "Tolls",
        "Permits / licensing", "Truck wash", "Parking", "Broker fee",
        "ELD / subscription", "Office", "Other",
    ]
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="expenses")
    date = models.DateField()
    category = models.CharField(
        max_length=60, default="Fuel",
        help_text="Pick a suggestion or type your own category.",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=120, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    load = models.ForeignKey(Load, on_delete=models.SET_NULL, null=True, blank=True)
    receipt = models.FileField(upload_to="expenses/", blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_category_display()} - ${self.amount} ({self.date})"


class Settlement(models.Model):
    """Driver wages for a pay period. Wages live here, not in Expense, to keep P&L clean."""
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="settlements")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="settlements")
    period_start = models.DateField()
    period_end = models.DateField()
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-period_end"]

    @property
    def net_pay(self):
        return self.gross_pay - self.deductions

    def __str__(self):
        return f"{self.driver} · {self.period_start} to {self.period_end}"


class Applicant(models.Model):
    """A driver who applied online via the company's hiring link."""
    STAGE_CHOICES = [
        ("applied", "Applied"),
        ("screening", "Screening (MVR / PSP)"),
        ("dq_file", "DQ file"),
        ("cleared", "Cleared / hired"),
        ("declined", "Declined"),
    ]
    CDL_CLASS_CHOICES = [("A", "Class A"), ("B", "Class B"), ("C", "Class C")]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="applicants")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    current_address = models.CharField("Current address", max_length=200, blank=True)
    address_history = models.TextField("Address history (last 3 years)", blank=True)
    cdl_number = models.CharField("CDL number", max_length=40, blank=True)
    cdl_class = models.CharField("CDL class", max_length=1, choices=CDL_CLASS_CHOICES, blank=True)
    cdl_state = models.CharField("CDL state", max_length=20, blank=True)
    years_experience = models.PositiveIntegerField("Years of experience", null=True, blank=True)
    employment_history = models.TextField("Employment history (last 10 years)", blank=True)
    accidents = models.TextField("Accident / violation history", blank=True)

    cdl_file = models.FileField("CDL (front & back)", upload_to="applicants/cdl/", blank=True)
    medical_file = models.FileField("Medical certificate", upload_to="applicants/medical/", blank=True)
    other_file = models.FileField("Other document", upload_to="applicants/other/", blank=True)

    consent = models.BooleanField(
        "Authorizes MVR, PSP, drug/alcohol & Clearinghouse checks", default=False)
    signature = models.CharField("Signature (typed full name)", max_length=100, blank=True)

    stage = models.CharField(max_length=12, choices=STAGE_CHOICES, default="applied")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_stage_display()})"


class ComplianceDocument(models.Model):
    """A document in a driver's qualification file, tracked with an expiry date."""
    DOC_TYPE_CHOICES = [
        ("application", "Employment application"),
        ("mvr", "Motor Vehicle Record (MVR)"),
        ("medical", "Medical certificate"),
        ("clearinghouse", "Clearinghouse query"),
        ("drug_test", "Drug / alcohol test"),
        ("eldt", "ELDT certificate"),
        ("road_test", "Road test / CDL equivalency"),
        ("safety_history", "Safety performance history"),
        ("w9", "W-9 (contractor)"),
        ("other", "Other"),
    ]
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="documents")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True,
        help_text="Leave blank if this document does not expire.")
    file = models.FileField(upload_to="compliance/", blank=True)
    verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["expiry_date"]

    def save(self, *args, **kwargs):
        if not self.company_id and self.driver_id:
            self.company = self.driver.company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver} - {self.get_doc_type_display()}"


class ActivityLog(models.Model):
    """A running record of activity in the system (the in-app notification feed)."""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="activity")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, blank=True)
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text


class NotificationRule(models.Model):
    """Which events notify you, and how. You control these in the admin."""
    EVENT_CHOICES = [
        ("load_created", "Load booked"),
        ("payment_updated", "Load payment status changed"),
        ("application_received", "New driver application"),
        ("expense_added", "Expense added"),
        ("settlement_created", "Driver settlement created"),
        ("doc_expiring", "Document expiring soon"),
    ]
    event = models.CharField(max_length=40, choices=EVENT_CHOICES, unique=True)
    in_app = models.BooleanField("In-app", default=True)
    email = models.BooleanField("Email", default=False)
    sms = models.BooleanField("Text (coming soon)", default=False)

    class Meta:
        ordering = ["event"]

    def __str__(self):
        return self.get_event_display()


def notify(event, text, company=None):
    """Record an in-app activity and, if enabled + configured, send an email."""
    from django.conf import settings
    from django.core.mail import send_mail
    try:
        rule = NotificationRule.objects.filter(event=event).first()
    except Exception:
        rule = None
    if rule is None or rule.in_app:
        from .middleware import get_current_user
        u = get_current_user()
        ActivityLog.objects.create(company=company, category=event, text=text,
                                   user=u if getattr(u, "is_authenticated", False) else None)
    if rule and rule.email and getattr(settings, "EMAIL_HOST", ""):
        admins = list(User.objects.filter(is_superuser=True)
                      .exclude(email="").values_list("email", flat=True))
        if admins:
            send_mail(f"[Fleetline] {rule.get_event_display()}", text,
                      settings.DEFAULT_FROM_EMAIL, admins, fail_silently=True)


# ---- auto-logging signals ----
from django.db.models.signals import pre_save

@receiver(post_save, sender=Load)
def _log_load(sender, instance, created, **kwargs):
    if created:
        notify("load_created",
               f"Load {instance.reference} booked ({instance.origin} -> {instance.destination})",
               instance.company)
    elif getattr(instance, "_old_payment", None) and instance._old_payment != instance.payment_status:
        notify("payment_updated",
               f"Load {instance.reference} payment: {instance.get_payment_status_display()}",
               instance.company)

@receiver(pre_save, sender=Load)
def _stash_payment(sender, instance, **kwargs):
    if instance.pk:
        old = Load.objects.filter(pk=instance.pk).values_list("payment_status", flat=True).first()
        instance._old_payment = old

@receiver(post_save, sender=Applicant)
def _log_applicant(sender, instance, created, **kwargs):
    if created:
        notify("application_received",
               f"New driver application from {instance.first_name} {instance.last_name}",
               instance.company)

@receiver(post_save, sender=Expense)
def _log_expense(sender, instance, created, **kwargs):
    if created:
        notify("expense_added",
               f"{instance.category} expense ${instance.amount} added", instance.company)

@receiver(post_save, sender=Settlement)
def _log_settlement(sender, instance, created, **kwargs):
    if created:
        notify("settlement_created",
               f"Settlement for {instance.driver}: ${instance.net_pay}", instance.company)


class Broker(models.Model):
    """A broker/customer you haul for. Loads link to a broker; works across companies."""
    name = models.CharField(max_length=140)
    mc_number = models.CharField("MC number", max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FuelTransaction(models.Model):
    """A fuel-card purchase. Imported from a CSV export, or later via the WEX API."""
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="fuel")
    date = models.DateField(null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    card_last4 = models.CharField("Card (last 4)", max_length=8, blank=True)
    location = models.CharField(max_length=160, blank=True)
    gallons = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.CharField(max_length=20, default="csv")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Fuel ${self.amount} on {self.date}"


class TimeEntry(models.Model):
    """A check-in / check-out record for a team member (the time clock)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_entries")
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-clock_in"]

    @property
    def hours(self):
        end = self.clock_out or __import__("django.utils.timezone", fromlist=["now"]).now()
        return round((end - self.clock_in).total_seconds() / 3600, 2)

    @property
    def is_open(self):
        return self.clock_out is None

    def __str__(self):
        return f"{self.user.username} @ {self.clock_in:%Y-%m-%d %H:%M}"

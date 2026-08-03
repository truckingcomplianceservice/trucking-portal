"""
Phase 1 data model: the foundation of the trucking portal.

Companies (each with its own MC/DOT/CA and factor), Drivers, Vehicles,
Loads, and user Profiles that control role and which companies a person
can access.
"""
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
    factor = models.CharField(max_length=10, choices=FACTOR_CHOICES, default="None")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("dispatcher", "Dispatcher"),
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

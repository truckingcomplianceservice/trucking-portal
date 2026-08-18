"""Views: P&L, protected media, public hiring form, compliance dashboard, hiring links."""
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.static import serve
from django.conf import settings
from .models import (Company, Load, Expense, Settlement, Driver, Vehicle, Applicant,
                     ComplianceDocument, Broker, FuelTransaction, RentalContract, VehicleDocument, notify)


def require_section(section):
    """Block direct access to a section a user's role isn't allowed to reach."""
    from functools import wraps

    def deco(viewfunc):
        @wraps(viewfunc)
        def wrapper(request, *args, **kwargs):
            from django.contrib import messages
            from .access import can
            if not can(request.user, section):
                messages.error(request, "You don't have access to that area.")
                return redirect("dashboard")
            return viewfunc(request, *args, **kwargs)
        return wrapper
    return deco


# ---------------- P&L ----------------
@login_required
def pnl_report(request):
    user = request.user
    companies = Company.objects.all()
    if not user.is_superuser:
        companies = companies.filter(pk__in=user.profile.companies.all())
    rows, tr, te, tw = [], 0, 0, 0
    for c in companies:
        rev = Load.objects.filter(company=c).aggregate(s=Sum("rate"))["s"] or 0
        exp = Expense.objects.filter(company=c).aggregate(s=Sum("amount"))["s"] or 0
        wag = sum(s.net_pay for s in Settlement.objects.filter(company=c))
        rows.append({"name": c.name, "mc": c.mc_number, "rev": rev, "exp": exp,
                     "wag": wag, "net": rev - exp - wag})
        tr += rev; te += exp; tw += wag
    totals = {"rev": tr, "exp": te, "wag": tw, "net": tr - te - tw}
    return render(request, "operations/pnl.html", {"rows": rows, "totals": totals})


@login_required
def protected_media(request, path):
    return serve(request, path, document_root=settings.MEDIA_ROOT)


# ---------------- Public hiring form ----------------
class ApplicantForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label="I authorize this carrier to obtain my MVR, PSP, drug & alcohol testing "
              "records, and Clearinghouse information as part of this application.")

    class Meta:
        model = Applicant
        fields = ["first_name", "last_name", "phone", "email", "current_address",
                  "address_history", "cdl_number", "cdl_class", "cdl_state",
                  "years_experience", "employment_history", "accidents",
                  "cdl_file", "medical_file", "other_file", "consent", "signature"]
        widgets = {
            "address_history": forms.Textarea(attrs={"rows": 3}),
            "employment_history": forms.Textarea(attrs={"rows": 4}),
            "accidents": forms.Textarea(attrs={"rows": 2}),
        }


def apply_view(request, token):
    company = get_object_or_404(Company, apply_token=token, active=True)
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.company = company
            applicant.stage = "applied"
            applicant.save()
            return redirect("apply_thanks")
    else:
        form = ApplicantForm()
    return render(request, "operations/apply.html", {"form": form, "company": company})


def apply_thanks(request):
    return render(request, "operations/apply_thanks.html")


# ---------------- Compliance dashboard ----------------
@login_required
def compliance_report(request):
    user = request.user
    companies = Company.objects.all()
    if not user.is_superuser:
        companies = companies.filter(pk__in=user.profile.companies.all())
    today = datetime.date.today()
    items = []

    def add(holder, company, kind, expiry):
        if not expiry:
            return
        days = (expiry - today).days
        items.append({"holder": holder, "company": company, "kind": kind,
                      "expiry": expiry, "days": days})

    for d in Driver.objects.filter(company__in=companies):
        add(f"{d.first_name} {d.last_name}", d.company.name, "CDL", d.cdl_expiry)
        add(f"{d.first_name} {d.last_name}", d.company.name, "Medical card", d.medical_expiry)
    for v in Vehicle.objects.filter(company__in=companies):
        add(f"Unit {v.unit_number}", v.company.name, "DOT inspection", v.inspection_expiry)
        add(f"Unit {v.unit_number}", v.company.name, "Plate / registration", v.registration_expiry)
        add(f"Unit {v.unit_number}", v.company.name, "Service due", v.next_service_date)
    for doc in ComplianceDocument.objects.filter(company__in=companies):
        add(str(doc.driver), doc.company.name, doc.get_doc_type_display(), doc.expiry_date)

    items.sort(key=lambda x: x["days"])
    overdue = [i for i in items if i["days"] < 0]
    soon = [i for i in items if 0 <= i["days"] <= 30]
    ok = [i for i in items if i["days"] > 30]
    return render(request, "operations/compliance.html",
                  {"overdue": overdue, "soon": soon, "ok": ok, "count": len(overdue) + len(soon)})


@login_required
def hiring_links(request):
    user = request.user
    companies = Company.objects.all()
    if not user.is_superuser:
        companies = companies.filter(pk__in=user.profile.companies.all())
    rows = [{"name": c.name,
             "url": request.build_absolute_uri(f"/apply/{c.apply_token}/")} for c in companies]
    return render(request, "operations/hiring_links.html", {"rows": rows})


# ---------------- Phase 4: reports index, tax, 1099, factoring, activity ----------------
import datetime as _dt
from django.http import Http404
from .models import ActivityLog, MaintenanceRecord


def _scoped_companies(request):
    companies = Company.objects.all()
    if not request.user.is_superuser:
        companies = companies.filter(pk__in=request.user.profile.companies.all())
    return companies


@login_required
def reports_index(request):
    return render(request, "operations/reports_index.html")


@require_section("tax")
@login_required
def tax_report(request):
    companies = _scoped_companies(request)
    year = int(request.GET.get("year", _dt.date.today().year))
    summary, contractors = [], []
    for c in companies:
        rev = Load.objects.filter(company=c, pickup_date__year=year).aggregate(s=Sum("rate"))["s"] or 0
        exp = Expense.objects.filter(company=c, date__year=year).aggregate(s=Sum("amount"))["s"] or 0
        summary.append({"name": c.name, "ein": c.ein, "rev": rev, "exp": exp, "net": rev - exp})
    for d in Driver.objects.filter(company__in=companies, tax_status="1099"):
        paid = Settlement.objects.filter(driver=d, period_end__year=year).aggregate(s=Sum("gross_pay"))["s"] or 0
        contractors.append({"id": d.id, "name": f"{d.first_name} {d.last_name}",
                            "company": d.company.name, "paid": paid,
                            "over": paid >= 600, "w9": bool(d.tax_id)})
    years = list(range(_dt.date.today().year, _dt.date.today().year - 4, -1))
    return render(request, "operations/tax.html",
                  {"summary": summary, "contractors": contractors, "year": year, "years": years})


@login_required
def generate_1099(request, driver_id):
    year = int(request.GET.get("year", _dt.date.today().year))
    companies = _scoped_companies(request)
    try:
        d = Driver.objects.get(pk=driver_id, company__in=companies)
    except Driver.DoesNotExist:
        raise Http404
    paid = Settlement.objects.filter(driver=d, period_end__year=year).aggregate(s=Sum("gross_pay"))["s"] or 0
    return render(request, "operations/form_1099.html",
                  {"d": d, "company": d.company, "paid": paid, "year": year})


@login_required
def factoring_report(request):
    companies = _scoped_companies(request)
    groups = []
    for c in companies:
        loads = Load.objects.filter(company=c).exclude(payment_status__in=["closed"])
        outstanding = loads.exclude(payment_status="unpaid").aggregate(s=Sum("rate"))["s"] or 0
        rows = [{"ref": l.reference, "customer": l.customer, "rate": l.rate,
                 "status": l.get_payment_status_display(), "code": l.payment_status}
                for l in loads.order_by("payment_status")]
        groups.append({"name": c.name, "factor": c.factor, "outstanding": outstanding, "rows": rows})
    return render(request, "operations/factoring.html", {"groups": groups})


@login_required
def activity_feed(request):
    companies = _scoped_companies(request)
    logs = ActivityLog.objects.filter(company__in=companies)[:200] if not request.user.is_superuser \
        else ActivityLog.objects.all()[:200]
    return render(request, "operations/activity.html", {"logs": logs})


# ---------------- Phase 5: branded dashboard ----------------
def _expiring_items(companies):
    today = _dt.date.today()
    items = []
    def add(holder, kind, expiry):
        if expiry:
            items.append({"holder": holder, "kind": kind, "expiry": expiry,
                          "days": (expiry - today).days})
    for d in Driver.objects.filter(company__in=companies):
        add(f"{d.first_name} {d.last_name}", "CDL", d.cdl_expiry)
        add(f"{d.first_name} {d.last_name}", "Medical card", d.medical_expiry)
    for v in Vehicle.objects.filter(company__in=companies):
        add(f"Unit {v.unit_number}", "Inspection", v.inspection_expiry)
        add(f"Unit {v.unit_number}", "Plate / registration", v.registration_expiry)
        add(f"Unit {v.unit_number}", "Service due", v.next_service_date)
    for rc in RentalContract.objects.filter(company__in=companies, active=True):
        add(f"Unit {rc.vehicle.unit_number}", "Rental contract ending", rc.end_date)
    for vd in VehicleDocument.objects.filter(company__in=companies).exclude(expiry_date=None):
        add(f"Unit {vd.vehicle.unit_number}", vd.label, vd.expiry_date)
    for doc in ComplianceDocument.objects.filter(company__in=companies):
        add(str(doc.driver), doc.get_doc_type_display(), doc.expiry_date)
    items.sort(key=lambda x: x["days"])
    return items


@login_required
def dashboard(request):
    companies = _scoped_companies(request)
    active_loads = Load.objects.filter(
        company__in=companies, status__in=["booked", "dispatched", "in_transit"]).count()
    driver_count = Driver.objects.filter(company__in=companies, status="active").count()
    outstanding = Load.objects.filter(
        company__in=companies,
        payment_status__in=["submitted", "advanced", "reserve_released"]
    ).aggregate(s=Sum("rate"))["s"] or 0
    exp_items = _expiring_items(companies)
    alerts = [i for i in exp_items if i["days"] <= 30]
    recent_loads = Load.objects.filter(company__in=companies).select_related("company", "driver")[:6]
    recent_activity = (ActivityLog.objects.all()[:8] if request.user.is_superuser
                       else ActivityLog.objects.filter(company__in=companies)[:8])
    return render(request, "operations/dashboard.html", {
        "active_loads": active_loads, "driver_count": driver_count,
        "outstanding": outstanding, "alert_count": len(alerts),
        "alerts": alerts[:6], "recent_loads": recent_loads,
        "recent_activity": recent_activity, "company_count": companies.count(),
    })


# ================= Phase 5: full custom section pages =================
from django.shortcuts import get_object_or_404 as _get

STATUS_CLASS = {"booked":"c-gray","dispatched":"c-blue","in_transit":"c-blue",
                "delivered":"c-green","invoiced":"c-warn","paid":"c-green"}
PAY_CLASS = {"unpaid":"c-gray","submitted":"c-warn","advanced":"c-blue",
             "reserve_released":"c-green","closed":"c-green"}


def _active(request):
    val = request.GET.get("company")
    if val is not None:
        request.session["active_company"] = val
    return request.session.get("active_company", "all")


def _companies(request):
    cs = Company.objects.all()
    if not request.user.is_superuser:
        cs = cs.filter(pk__in=request.user.profile.companies.all())
    ac = _active(request)
    if ac and ac != "all":
        cs = cs.filter(pk=ac)
    return cs


def _exp_chip(expiry):
    if not expiry:
        return {"cls": "c-gray", "label": "—"}
    days = (expiry - _dt.date.today()).days
    if days < 0:
        return {"cls": "c-red", "label": f"Expired {abs(days)}d"}
    if days <= 30:
        return {"cls": "c-warn", "label": f"{days}d left"}
    return {"cls": "c-green", "label": "Valid"}


@require_section("dispatch")
@login_required
def app_loads(request):
    cs = _companies(request)
    base = Load.objects.filter(company__in=cs).select_related("company", "driver", "vehicle", "broker")
    # status counts (over all company loads, so tabs always show totals)
    counts = {"all": base.count()}
    for code, _label in Load.STATUS_CHOICES:
        counts[code] = base.filter(status=code).count()
    # read filters
    f = {k: request.GET.get(k, "").strip() for k in
         ["status", "ref", "customer", "driver", "truck", "origin", "destination", "start", "end"]}
    loads = base
    if f["status"] and f["status"] != "all":
        loads = loads.filter(status=f["status"])
    if f["ref"]:
        loads = loads.filter(Q(reference__icontains=f["ref"]) | Q(invoice_number__icontains=f["ref"]))
    if f["customer"]:
        loads = loads.filter(Q(customer__icontains=f["customer"]) | Q(broker__name__icontains=f["customer"]))
    if f["driver"]:
        loads = loads.filter(Q(driver__first_name__icontains=f["driver"]) |
                             Q(driver__last_name__icontains=f["driver"]))
    if f["truck"]:
        loads = loads.filter(vehicle__unit_number__icontains=f["truck"])
    if f["origin"]:
        loads = loads.filter(origin__icontains=f["origin"])
    if f["destination"]:
        loads = loads.filter(destination__icontains=f["destination"])
    def parse(d):
        try: return _dt.date.fromisoformat(d)
        except ValueError: return None
    if parse(f["start"]): loads = loads.filter(pickup_date__gte=parse(f["start"]))
    if parse(f["end"]): loads = loads.filter(pickup_date__lte=parse(f["end"]))
    rows = [{"o": l, "sc": STATUS_CLASS.get(l.status, "c-gray"),
             "pc": PAY_CLASS.get(l.payment_status, "c-gray")} for l in loads]
    return render(request, "operations/app_loads.html", {
        "rows": rows, "counts": counts, "f": f,
        "statuses": Load.STATUS_CHOICES, "shown": len(rows), "total": counts["all"],
    })


@require_section("dispatch")
@login_required
def app_load_detail(request, pk):
    l = _get(Load, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_load_detail.html",
                  {"l": l, "sc": STATUS_CLASS.get(l.status, "c-gray"),
                   "pc": PAY_CLASS.get(l.payment_status, "c-gray"),
                   "thread_notes": l.team_notes.select_related("author"),
                   "note_company_id": l.company_id, "note_field": "load",
                   "note_obj_id": l.id, "note_next": f"/app/loads/{l.id}/"})


@require_section("drivers")
@login_required
def app_drivers(request):
    cs = _companies(request)
    drivers = Driver.objects.filter(company__in=cs).select_related("company")
    rows = [{"o": d, "cdl": _exp_chip(d.cdl_expiry), "med": _exp_chip(d.medical_expiry),
             "dqf": _dqf_overall(d),
             "initials": (d.first_name[:1] + d.last_name[:1]).upper()} for d in drivers]
    return render(request, "operations/app_drivers.html", {"rows": rows})


@require_section("drivers")
@login_required
def app_driver_detail(request, pk):
    d = _get(Driver, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_driver_detail.html",
                  {"d": d, "cdl": _exp_chip(d.cdl_expiry), "med": _exp_chip(d.medical_expiry),
                   "thread_notes": d.team_notes.select_related("author"),
                   "note_company_id": d.company_id, "note_field": "driver",
                   "note_obj_id": d.id, "note_next": f"/app/drivers/{d.id}/"})


def _service_chip(v):
    """Maintenance status from miles-to-service and/or next service date."""
    today = _dt.date.today()
    mts = v.miles_to_service
    # mileage-based
    if mts is not None:
        if mts <= 0:
            return {"cls": "c-red", "label": f"Overdue {abs(mts):,} mi"}
        if mts <= 1500:
            return {"cls": "c-warn", "label": f"{mts:,} mi left"}
        return {"cls": "c-green", "label": f"{mts:,} mi left"}
    # date-based
    if v.next_service_date:
        days = (v.next_service_date - today).days
        if days < 0:
            return {"cls": "c-red", "label": f"Overdue {abs(days)}d"}
        if days <= 30:
            return {"cls": "c-warn", "label": f"Due in {days}d"}
        return {"cls": "c-green", "label": "Scheduled"}
    return {"cls": "c-gray", "label": "Not tracked"}


@require_section("vehicles")
@login_required
def app_vehicles(request):
    cs = _companies(request)
    vehicles = Vehicle.objects.filter(company__in=cs).select_related("company")
    rows = [{"o": v, "insp": _exp_chip(v.inspection_expiry),
             "reg": _exp_chip(v.registration_expiry), "service": _service_chip(v)} for v in vehicles]
    return render(request, "operations/app_vehicles.html", {"rows": rows})


@require_section("vehicles")
@login_required
def app_vehicle_detail(request, pk):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    records = v.maintenance.all()
    today = _dt.date.today()
    total_all = sum((r.total for r in records), 0)
    total_year = sum((r.total for r in records if r.date and r.date.year == today.year), 0)
    total_month = sum((r.total for r in records if r.date and r.date.year == today.year
                       and r.date.month == today.month), 0)
    months = {}
    for r in records:
        if r.date:
            key = r.date.strftime("%Y-%m")
            months[key] = months.get(key, 0) + r.total
    monthly = [{"month": _dt.datetime.strptime(k, "%Y-%m").strftime("%b %Y"), "total": t}
               for k, t in sorted(months.items(), reverse=True)]
    docs = [{"o": d, "chip": _exp_chip(d.expiry_date) if d.expiry_date else None}
            for d in v.documents.all()]
    return render(request, "operations/app_vehicle_detail.html",
                  {"v": v, "insp": _exp_chip(v.inspection_expiry),
                   "reg": _exp_chip(v.registration_expiry), "service": _service_chip(v),
                   "records": records, "total_all": total_all, "total_year": total_year,
                   "total_month": total_month, "monthly": monthly, "today": today.isoformat(),
                   "docs": docs, "doc_types": VehicleDocument.DOC_TYPES})


@login_required
def maintenance_add(request, pk):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    if request.method == "POST":
        def num(x):
            try: return float(str(x).replace("$", "").replace(",", "") or 0)
            except ValueError: return 0
        def date(x):
            try: return _dt.date.fromisoformat(x)
            except (ValueError, TypeError): return _dt.date.today()
        part = request.POST.get("part", "").strip()
        if part:
            rec = MaintenanceRecord.objects.create(
                company=v.company, vehicle=v, date=date(request.POST.get("date")),
                part=part, vendor=request.POST.get("vendor", "").strip(),
                odometer=int(num(request.POST.get("odometer"))) or None,
                parts_cost=num(request.POST.get("parts_cost")),
                labor_cost=num(request.POST.get("labor_cost")),
                receipt=request.FILES.get("receipt"),
                notes=request.POST.get("notes", "").strip())
            ActivityLog.objects.create(category="maintenance", user=request.user, company=v.company,
                text=f"Logged service on Unit {v.unit_number}: {part} (${rec.total})")
    return redirect("app_vehicle_detail", pk=v.id)


@require_section("hiring")
@login_required
def app_hiring(request):
    cs = _companies(request)
    stages = [("applied", "Applied"), ("screening", "Screening"),
              ("dq_file", "DQ file"), ("cleared", "Cleared / hired")]
    cols = []
    for code, label in stages:
        apps = Applicant.objects.filter(company__in=cs, stage=code)
        cols.append({"label": label, "apps": apps, "count": apps.count()})
    return render(request, "operations/app_hiring.html", {"cols": cols})


@require_section("compliance")
@login_required
def app_compliance(request):
    items = _expiring_items(_companies(request))
    overdue = [i for i in items if i["days"] < 0]
    soon = [i for i in items if 0 <= i["days"] <= 30]
    ok = [i for i in items if i["days"] > 30]
    return render(request, "operations/app_compliance.html",
                  {"overdue": overdue, "soon": soon, "ok": ok, "count": len(overdue) + len(soon)})


@require_section("accounting")
@login_required
def app_accounting(request):
    cs = _companies(request)
    rows, tr, te, tw = [], 0, 0, 0
    for c in cs:
        rev = Load.objects.filter(company=c).aggregate(s=Sum("rate"))["s"] or 0
        exp = Expense.objects.filter(company=c).aggregate(s=Sum("amount"))["s"] or 0
        wag = sum(s.net_pay for s in Settlement.objects.filter(company=c))
        rows.append({"name": c.name, "rev": rev, "exp": exp, "wag": wag, "net": rev - exp - wag})
        tr += rev; te += exp; tw += wag
    expenses = Expense.objects.filter(company__in=cs).select_related("company")[:12]
    settlements = Settlement.objects.filter(company__in=cs).select_related("driver", "company")[:8]
    totals = {"rev": tr, "exp": te, "wag": tw, "net": tr - te - tw}
    return render(request, "operations/app_accounting.html",
                  {"rows": rows, "totals": totals, "expenses": expenses, "settlements": settlements,
                   "companies": cs,
                   "vehicles": Vehicle.objects.filter(company__in=cs).order_by("unit_number"),
                   "drivers": Driver.objects.filter(company__in=cs).order_by("first_name")})


@require_section("accounting")
@login_required
def expense_add(request):
    """Add an expense (with optional receipt) from the Accounting page."""
    cs = _companies(request)
    if request.method == "POST":
        company = cs.filter(pk=request.POST.get("company")).first() or cs.first()
        try:
            import os
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "expenses"), exist_ok=True)
            Expense.objects.create(
                company=company,
                date=_parse_date(request.POST.get("date", "")) or _dt.date.today(),
                category=request.POST.get("category", "").strip() or "Other",
                amount=round(_num(request.POST.get("amount", "0")), 2),
                vendor=request.POST.get("vendor", "").strip(),
                vehicle=Vehicle.objects.filter(pk=request.POST.get("vehicle"), company__in=cs).first(),
                driver=Driver.objects.filter(pk=request.POST.get("driver"), company__in=cs).first(),
                receipt=request.FILES.get("receipt"))
            _messages.success(request, "Expense added.")
        except Exception as e:
            _messages.error(request, f"Could not add the expense: {e}")
    return redirect("app_accounting")


@require_section("accounting")
@login_required
def expense_receipt(request, pk):
    """Attach/replace a receipt on an existing expense, or delete the expense."""
    e = _get(Expense, pk=pk, company__in=_companies(request))
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            e.delete(); _messages.success(request, "Expense removed.")
        elif request.FILES.get("receipt"):
            try:
                import os
                os.makedirs(os.path.join(settings.MEDIA_ROOT, "expenses"), exist_ok=True)
                e.receipt = request.FILES["receipt"]; e.save()
                _messages.success(request, "Receipt attached.")
            except Exception as ex:
                _messages.error(request, f"Could not attach receipt: {ex}")
    return redirect("app_accounting")


def _companies_all(request):
    """All companies the user may access (ignores the switcher, for detail lookups)."""
    cs = Company.objects.all()
    if not request.user.is_superuser:
        cs = cs.filter(pk__in=request.user.profile.companies.all())
    return cs


# ================= Report builder: date range + driver/company search =================
from django.db.models import Q as _Q


@login_required
def report_builder(request):
    companies = _companies_all(request)
    kind = request.GET.get("kind", "loads")
    start = request.GET.get("start", "")
    end = request.GET.get("end", "")
    company = request.GET.get("company", "")
    q = request.GET.get("q", "").strip()

    def parse(d):
        try:
            return _dt.date.fromisoformat(d)
        except ValueError:
            return None
    sd, ed = parse(start), parse(end)

    headers, rows, total, total_label, submitted = [], [], 0, "", bool(request.GET)

    if kind == "loads":
        headers = ["Date", "Load", "Company", "Route", "Driver", "Rate", "Status"]
        total_label = "Total rate"
        qs = Load.objects.filter(company__in=companies).select_related("company", "driver")
        if sd: qs = qs.filter(pickup_date__gte=sd)
        if ed: qs = qs.filter(pickup_date__lte=ed)
        if company: qs = qs.filter(company_id=company)
        if q:
            qs = qs.filter(_Q(driver__first_name__icontains=q) | _Q(driver__last_name__icontains=q)
                           | _Q(driver__phone__icontains=q))
        for l in qs.order_by("-pickup_date"):
            rows.append([l.pickup_date or "—", l.reference, l.company.name,
                         f"{l.origin} → {l.destination}", str(l.driver or "—"),
                         f"${l.rate:,.2f}", l.get_status_display()])
            total += l.rate

    elif kind == "settlements":
        headers = ["Period end", "Driver", "Company", "Gross", "Deductions", "Net"]
        total_label = "Total net pay"
        qs = Settlement.objects.filter(company__in=companies).select_related("company", "driver")
        if sd: qs = qs.filter(period_end__gte=sd)
        if ed: qs = qs.filter(period_end__lte=ed)
        if company: qs = qs.filter(company_id=company)
        if q:
            qs = qs.filter(_Q(driver__first_name__icontains=q) | _Q(driver__last_name__icontains=q)
                           | _Q(driver__phone__icontains=q))
        for s in qs.order_by("-period_end"):
            rows.append([s.period_end, str(s.driver), s.company.name,
                         f"${s.gross_pay:,.2f}", f"${s.deductions:,.2f}", f"${s.net_pay:,.2f}"])
            total += s.net_pay

    elif kind == "expenses":
        headers = ["Date", "Category", "Company", "Vendor", "Driver", "Amount"]
        total_label = "Total expenses"
        qs = Expense.objects.filter(company__in=companies).select_related("company", "driver")
        if sd: qs = qs.filter(date__gte=sd)
        if ed: qs = qs.filter(date__lte=ed)
        if company: qs = qs.filter(company_id=company)
        if q:
            qs = qs.filter(_Q(driver__first_name__icontains=q) | _Q(driver__last_name__icontains=q)
                           | _Q(driver__phone__icontains=q) | _Q(vendor__icontains=q))
        for e in qs.order_by("-date"):
            rows.append([e.date, e.category, e.company.name, e.vendor or "—",
                         str(e.driver or "—"), f"${e.amount:,.2f}"])
            total += e.amount

    return render(request, "operations/app_report_builder.html", {
        "headers": headers, "rows": rows, "total": total, "total_label": total_label,
        "kind": kind, "start": start, "end": end, "company_sel": company, "q": q,
        "all_companies": companies, "submitted": submitted, "count": len(rows),
    })


# ================= Brokers + Fuel (with CSV import) =================
import csv as _csv
import io as _io
from django.db.models import Count as _Count


@require_section("brokers")
@login_required
def app_brokers(request):
    cs = _companies(request)
    # per-company broker summary
    per_company = []
    for c in cs:
        loads = Load.objects.filter(company=c)
        n_brokers = loads.exclude(broker__isnull=True).values("broker").distinct().count()
        per_company.append({"name": c.name, "brokers": n_brokers,
                            "loads": loads.count(),
                            "rev": loads.aggregate(s=Sum("rate"))["s"] or 0})
    # broker table (across the scoped companies)
    brokers = []
    for b in Broker.objects.all():
        bl = Load.objects.filter(broker=b, company__in=cs)
        if bl.exists():
            companies_served = ", ".join(sorted({l.company.name for l in bl}))
            brokers.append({"o": b, "loads": bl.count(),
                            "rev": bl.aggregate(s=Sum("rate"))["s"] or 0,
                            "companies": companies_served})
    brokers.sort(key=lambda x: x["loads"], reverse=True)
    return render(request, "operations/app_brokers.html",
                  {"per_company": per_company, "brokers": brokers})


@require_section("fuel")
@login_required
def app_fuel(request):
    cs = _companies(request)
    txns = FuelTransaction.objects.filter(company__in=cs).select_related("company", "vehicle", "driver")
    vehicle_id = request.GET.get("vehicle", "")
    start = request.GET.get("start", ""); end = request.GET.get("end", "")
    def parse(d):
        try: return _dt.date.fromisoformat(d)
        except ValueError: return None
    if vehicle_id:
        txns = txns.filter(vehicle_id=vehicle_id)
    sd, ed = parse(start), parse(end)
    if sd: txns = txns.filter(date__gte=sd)
    if ed: txns = txns.filter(date__lte=ed)
    total_amt = txns.aggregate(s=Sum("amount"))["s"] or 0
    total_gal = txns.aggregate(s=Sum("gallons"))["s"] or 0
    qs = f"vehicle={vehicle_id}&start={start}&end={end}"
    return render(request, "operations/app_fuel.html",
                  {"txns": txns[:300], "total_amt": total_amt, "total_gal": total_gal,
                   "vehicles": Vehicle.objects.filter(company__in=cs), "vehicle_id": vehicle_id,
                   "start": start, "end": end, "qs": qs, "count": txns.count(),
                   "drivers": Driver.objects.filter(company__in=cs).order_by("first_name")})


@require_section("fuel")
@login_required
def fuel_add(request):
    """Add a fuel transaction manually, optionally with a receipt/invoice attached."""
    cs = _companies(request)
    if request.method == "POST":
        company = cs.filter(pk=request.POST.get("company")).first() or cs.first()
        try:
            import os
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "fuel_receipts"), exist_ok=True)
            FuelTransaction.objects.create(
                company=company,
                date=_parse_date(request.POST.get("date", "")) or _dt.date.today(),
                vehicle=Vehicle.objects.filter(pk=request.POST.get("vehicle"), company__in=cs).first(),
                driver=Driver.objects.filter(pk=request.POST.get("driver"), company__in=cs).first(),
                location=request.POST.get("location", "").strip()[:160],
                gallons=round(_num(request.POST.get("gallons", "0")), 2),
                amount=round(_num(request.POST.get("amount", "0")), 2),
                card_last4=request.POST.get("card_last4", "").strip()[-4:],
                receipt=request.FILES.get("receipt"),
                source="manual",
                notes=request.POST.get("notes", "").strip())
            _messages.success(request, "Fuel entry added.")
        except Exception as e:
            _messages.error(request, f"Could not add the entry: {e}")
    return redirect("app_fuel")


@require_section("fuel")
@login_required
def fuel_receipt(request, pk):
    """Attach or replace a receipt on an existing fuel transaction."""
    t = _get(FuelTransaction, pk=pk, company__in=_companies(request))
    if request.method == "POST" and request.FILES.get("receipt"):
        try:
            import os
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "fuel_receipts"), exist_ok=True)
            t.receipt = request.FILES["receipt"]; t.save()
            _messages.success(request, "Receipt attached.")
        except Exception as e:
            _messages.error(request, f"Could not attach receipt: {e}")
    return redirect("app_fuel")


def _find(header, *needles):
    """Return the column index best matching the needles, in PRIORITY order.
    Earlier needles win, regardless of column position (so 'amt' beats 'invoice')."""
    hls = [h.strip().lower() for h in header]
    for n in needles:
        for i, hl in enumerate(hls):
            if n in hl:
                return i
    return None


def _num(val):
    if val is None:
        return 0
    v = str(val).replace("$", "").replace(",", "").replace("(", "-").replace(")", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0


def _parse_date(val):
    val = (val or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return _dt.datetime.strptime(val, fmt).date()
        except ValueError:
            continue
    return None


@require_section("fuel")
@login_required
def fuel_import(request):
    companies = _companies_all(request)
    active = request.session.get("active_company", "all")
    ctx = {"companies": companies, "step": "upload", "active_id": str(active)}
    if request.method == "POST":
        stage = request.POST.get("stage")
        # STEP 1 -> read file, guess columns, show mapping
        if stage == "preview" and request.FILES.get("file"):
            raw = request.FILES["file"].read().decode("utf-8", errors="ignore")
            rows = list(_csv.reader(_io.StringIO(raw)))
            if rows:
                header = rows[0]
                def _find_unit(hdr):
                    hls = [h.strip().lower() for h in hdr]
                    for n in ("truck", "tractor", "vehicle", "asset"):
                        for i, hl in enumerate(hls):
                            if n in hl:
                                return i
                    for i, hl in enumerate(hls):   # a 'unit' column that isn't 'unit price'
                        if "unit" in hl and "price" not in hl:
                            return i
                    return None
                guess = {
                    "date": _find(header, "date"),
                    "amount": _find(header, "amt", "amount", "total", "net", "grand",
                                    "cost", "charge", "sale amt", "spent", "paid"),
                    "gallons": _find(header, "gallon", "qty", "quantity", "volume", "units"),
                    "location": _find(header, "merchant", "location", "site", "station", "vendor", "city"),
                    "card": _find(header, "card"),
                    "unit": _find_unit(header),
                }
                fielddefs = [("date", "Date"), ("amount", "Amount ($)"), ("gallons", "Gallons"),
                             ("location", "Location / merchant"), ("card", "Card number"),
                             ("unit", "Unit / truck #")]
                fields = []
                for fname, flabel in fielddefs:
                    gi = guess.get(fname)
                    opts = [{"idx": i, "header": h, "selected": (gi == i)} for i, h in enumerate(header)]
                    fields.append({"name": fname, "label": flabel, "options": opts})
                ctx.update({"step": "map", "fields": fields, "headers_list": header,
                            "sample": rows[1:4], "company_id": request.POST.get("company"),
                            "csv_data": raw})
        # STEP 2 -> import using the confirmed mapping
        elif stage == "import":
            company = _get(Company, pk=request.POST.get("company"),
                           pk__in=companies.values_list("pk", flat=True))
            raw = request.POST.get("csv_data", "")
            rows = list(_csv.reader(_io.StringIO(raw)))
            def col(key):
                v = request.POST.get(key, "")
                return int(v) if v not in ("", "none") else None
            idx = {k: col(k) for k in ["date", "amount", "gallons", "location", "card", "unit"]}
            existing = set()
            for t in FuelTransaction.objects.filter(company=company).values_list(
                    "date", "card_last4", "gallons", "amount", "location"):
                existing.add((t[0], t[1], round(float(t[2]), 2), round(float(t[3]), 2),
                              (t[4] or "").strip().lower()))
            created, skipped, dup = 0, 0, 0
            for row in rows[1:]:
                if not any(c.strip() for c in row):
                    continue
                def cell(key):
                    i = idx[key]
                    return row[i] if i is not None and i < len(row) else ""
                amount = round(_num(cell("amount")), 2); gallons = round(_num(cell("gallons")), 2)
                if amount == 0 and gallons == 0:
                    skipped += 1; continue
                date_val = _parse_date(cell("date"))
                card = cell("card").strip(); last4 = card[-4:] if card else ""
                loc = cell("location").strip()[:160]
                sig = (date_val, last4, gallons, amount, loc.strip().lower())
                if sig in existing:
                    dup += 1; continue
                vehicle = None; unit = cell("unit").strip()
                if unit:
                    vehicle = Vehicle.objects.filter(company=company, unit_number__iexact=unit).first()
                FuelTransaction.objects.create(
                    company=company, date=date_val, vehicle=vehicle,
                    card_last4=last4, location=loc,
                    gallons=gallons, amount=amount, source="csv")
                existing.add(sig)
                created += 1
            ctx.update({"step": "done", "result": {"created": created, "skipped": skipped,
                        "dup": dup, "company": company.name, "company_id": company.id}})
    return render(request, "operations/app_fuel_import.html", ctx)


@login_required
def fuel_report_pdf(request):
    cs = _companies(request)
    txns = FuelTransaction.objects.filter(company__in=cs).select_related("company", "vehicle")
    vehicle_id = request.GET.get("vehicle", "")
    start = request.GET.get("start", ""); end = request.GET.get("end", "")
    def parse(d):
        try: return _dt.date.fromisoformat(d)
        except ValueError: return None
    vlabel = "All trucks"
    if vehicle_id:
        txns = txns.filter(vehicle_id=vehicle_id)
        v = Vehicle.objects.filter(pk=vehicle_id).first()
        if v: vlabel = f"Unit {v.unit_number}"
    sd, ed = parse(start), parse(end)
    if sd: txns = txns.filter(date__gte=sd)
    if ed: txns = txns.filter(date__lte=ed)
    total_amt = txns.aggregate(s=Sum("amount"))["s"] or 0
    total_gal = txns.aggregate(s=Sum("gallons"))["s"] or 0
    pdf = _render_pdf("operations/pdf_fuel.html", {
        "txns": txns, "total_amt": f"{total_amt:,.2f}", "total_gal": f"{total_gal:,.1f}",
        "vlabel": vlabel, "start": start, "end": end,
        "company": cs.first().name if cs.count() == 1 else "All companies",
        "company_obj": cs.first() if cs.count() == 1 else None,
        "today": _dt.date.today()})
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'inline; filename="fuel-report.pdf"'
    return resp


# ================= Team management, time clock, who-did-what =================
from django.contrib.auth.models import User as _User, Group, Permission
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone as _tz
from django.utils.crypto import get_random_string as _rand
from django.contrib import messages as _messages
from .models import Profile, TimeEntry, ActivityLog

# role -> which operations models they can add/change/view
ROLE_PERMS = {
    "admin": "ALL", "manager": "ALL",
    "dispatcher": ["load", "driver", "vehicle", "broker"],
    "compliance": ["compliancedocument", "applicant", "driver", "vehicle"],
    "safety": ["compliancedocument", "driver", "vehicle"],
    "accountant": ["expense", "settlement", "fueltransaction", "invoice", "payment"],
    "billing": ["invoice", "payment", "expense", "load"],
    "driver": [],
}

# Only the owner (superuser) can touch these or delete anything.
OWNER_ONLY_MODELS = {"notificationrule"}


def _apply_role(user, role):
    """Give a team member a Django group with permissions matching their role.
    No one but the owner (superuser) gets delete rights or owner-only models."""
    user.is_staff = True
    user.save()
    group, _ = Group.objects.get_or_create(name=f"role_{role}")
    allowed = ROLE_PERMS.get(role, [])
    keep = []
    for p in Permission.objects.filter(content_type__app_label="operations"):
        model = p.content_type.model
        action = p.codename.split("_")[0]
        if model in OWNER_ONLY_MODELS:
            continue
        if action == "delete":            # delete = owner only
            continue
        if action not in ("add", "change", "view"):
            continue
        if allowed == "ALL" or model in allowed:
            keep.append(p.id)
    group.permissions.set(Permission.objects.filter(id__in=keep))
    user.groups.clear()
    user.groups.add(group)


def _is_manager(user):
    if user.is_superuser:
        return True
    try:
        return user.profile.role in ("admin", "manager")
    except Exception:
        return False


@require_section("team")
@login_required
def app_team(request):
    users = _User.objects.select_related("profile").order_by("-is_active", "first_name", "username")
    today = _tz.localdate()
    roster = []
    for u in users:
        try:
            prof = u.profile
        except Profile.DoesNotExist:
            prof = None
        open_entry = TimeEntry.objects.filter(user=u, clock_out__isnull=True).first()
        todays = TimeEntry.objects.filter(user=u, clock_in__date=today)
        hrs = round(sum(t.hours for t in todays), 2)
        roster.append({
            "u": u, "prof": prof,
            "role": prof.get_role_display() if prof else "—",
            "companies": ", ".join(c.name for c in prof.companies.all()) if prof else "",
            "on_clock": bool(open_entry), "today_hours": hrs,
            "initials": ((u.first_name[:1] + u.last_name[:1]).upper() or u.username[:2].upper()),
        })
    my_open = TimeEntry.objects.filter(user=request.user, clock_out__isnull=True).first()
    recent = ActivityLog.objects.select_related("user", "company")[:12]
    return render(request, "operations/app_team.html", {
        "roster": roster, "roles": Profile.ROLE_CHOICES,
        "all_companies": _companies_all(request), "my_open": my_open,
        "recent": recent, "can_manage": _is_manager(request.user),
    })


@login_required
def clock_toggle(request):
    if request.method == "POST":
        who = request.user.get_full_name() or request.user.username
        open_entry = TimeEntry.objects.filter(user=request.user, clock_out__isnull=True).first()
        if open_entry:
            open_entry.clock_out = _tz.now()
            open_entry.save()
            ActivityLog.objects.create(category="clock", user=request.user,
                text=f"{who} clocked out ({open_entry.hours}h)")
        else:
            TimeEntry.objects.create(user=request.user, clock_in=_tz.now())
            ActivityLog.objects.create(category="clock", user=request.user,
                text=f"{who} clocked in")
    return redirect("app_team")


@require_section("team")
@login_required
def team_add(request):
    if not _is_manager(request.user):
        _messages.error(request, "Only managers can add team members.")
        return redirect("app_team")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if not username or _User.objects.filter(username=username).exists():
            _messages.error(request, "That username is missing or already taken.")
            return redirect("app_team")
        u = _User.objects.create_user(
            username=username,
            email=request.POST.get("email", "").strip(),
            password=request.POST.get("password", "").strip() or _rand(10),
            first_name=request.POST.get("first_name", "").strip(),
            last_name=request.POST.get("last_name", "").strip(),
        )
        role = request.POST.get("role", "dispatcher")
        prof, _ = Profile.objects.get_or_create(user=u)
        prof.role = role
        prof.phone = request.POST.get("phone", "").strip()
        prof.save()
        prof.companies.set(request.POST.getlist("companies"))
        _apply_role(u, role)
        ActivityLog.objects.create(category="team", user=request.user,
            text=f"Added team member {u.get_full_name() or u.username} ({prof.get_role_display()})")
        _messages.success(request, f"Added {username}. They can log in with the password you set.")
    return redirect("app_team")


@require_section("team")
@login_required
def team_toggle_active(request, pk):
    if not _is_manager(request.user):
        return redirect("app_team")
    if request.method == "POST":
        u = _get(_User, pk=pk)
        if u != request.user:
            u.is_active = not u.is_active
            u.save()
            state = "reactivated" if u.is_active else "deactivated"
            ActivityLog.objects.create(category="team", user=request.user,
                text=f"{state.capitalize()} {u.get_full_name() or u.username}")
    return redirect("app_team")


@login_required
def app_timesheet(request):
    entries = TimeEntry.objects.select_related("user").all()[:200]
    return render(request, "operations/app_timesheet.html", {"entries": entries})


def go_home(request, exception=None):
    """Any unknown/broken link → send the person to the home page (login/dashboard)."""
    return redirect("/")


# ================= Driver Qualification File (DQF) — like a DQF portal =================
# FMCSA-style required items, in order. (label, doc_type)
DQF_CHECKLIST = [
    ("CDL license", "cdl"),
    ("Employment application", "application"),
    ("Medical examiner's certificate", "medical"),
    ("Motor Vehicle Record (MVR)", "mvr"),
    ("Annual review of driving record", "annual_review"),
    ("Road test / CDL equivalency", "road_test"),
    ("PSP report", "psp"),
    ("Pre-employment drug test", "drug_test"),
    ("Clearinghouse query", "clearinghouse"),
    ("Safety performance history", "safety_history"),
]


def _dqf_item_status(driver, doc_type):
    """Compute status for one checklist item from the driver's documents/fields."""
    doc = ComplianceDocument.objects.filter(driver=driver, doc_type=doc_type)\
        .order_by("-expiry_date", "-id").first()
    expiry = doc.expiry_date if doc else None
    if not doc:  # fall back to fields we already capture on the driver
        if doc_type == "cdl":
            expiry = driver.cdl_expiry
        elif doc_type == "medical":
            expiry = driver.medical_expiry
    present = bool(doc) or (expiry is not None)
    if not present:
        return {"cls": "c-red", "label": "Missing", "state": "missing", "doc": None, "expiry": None}
    if doc and not doc.verified:
        return {"cls": "c-warn", "label": "Pending review", "state": "pending", "doc": doc, "expiry": expiry}
    if expiry:
        days = (expiry - _dt.date.today()).days
        if days < 0:
            return {"cls": "c-red", "label": f"Expired {abs(days)}d", "state": "expired", "doc": doc, "expiry": expiry}
        if days <= 30:
            return {"cls": "c-warn", "label": f"Expiring {days}d", "state": "expiring", "doc": doc, "expiry": expiry}
    return {"cls": "c-green", "label": "Complete", "state": "complete", "doc": doc, "expiry": expiry}


def _dqf_overall(driver):
    states = [_dqf_item_status(driver, dt)["state"] for _, dt in DQF_CHECKLIST]
    if any(s in ("missing", "expired") for s in states):
        return {"cls": "c-red", "label": "Action needed"}
    if any(s in ("pending", "expiring") for s in states):
        return {"cls": "c-warn", "label": "Attention"}
    return {"cls": "c-green", "label": "Qualified"}


@login_required
def app_driver_dqf(request, pk):
    d = _get(Driver, pk=pk, company__in=_companies_all(request))
    items = []
    for label, dt in DQF_CHECKLIST:
        st = _dqf_item_status(d, dt)
        st.update({"label_name": label, "doc_type": dt})
        items.append(st)
    overall = _dqf_overall(d)
    upload_url = request.build_absolute_uri(f"/driver/{d.upload_token}/")
    complete = sum(1 for i in items if i["state"] == "complete")
    return render(request, "operations/app_driver_dqf.html", {
        "d": d, "items": items, "overall": overall, "upload_url": upload_url,
        "complete": complete, "total": len(items),
        "doc_types": ComplianceDocument.DOC_TYPE_CHOICES,
    })


@login_required
def dqf_approve(request, doc_id):
    if request.method == "POST":
        doc = _get(ComplianceDocument, pk=doc_id, company__in=_companies_all(request))
        doc.verified = True
        doc.save()
        ActivityLog.objects.create(category="compliance", user=request.user, company=doc.company,
            text=f"Approved {doc.get_doc_type_display()} for {doc.driver}")
        return redirect("app_driver_dqf", pk=doc.driver_id)
    return redirect("app_drivers")


@login_required
def dqf_reject(request, doc_id):
    if request.method == "POST":
        doc = _get(ComplianceDocument, pk=doc_id, company__in=_companies_all(request))
        drv = doc.driver_id
        doc.delete()
        return redirect("app_driver_dqf", pk=drv)
    return redirect("app_drivers")


# ---- public driver self-upload portal (no login) ----
def driver_upload(request, token):
    d = _get(Driver, upload_token=token)
    msg = None
    if request.method == "POST" and request.FILES.get("file"):
        doc_type = request.POST.get("doc_type", "other")
        expiry = request.POST.get("expiry_date") or None
        exp = None
        if expiry:
            try:
                exp = _dt.date.fromisoformat(expiry)
            except ValueError:
                exp = None
        ComplianceDocument.objects.create(
            company=d.company, driver=d, doc_type=doc_type, file=request.FILES["file"],
            expiry_date=exp, verified=False, notes="Uploaded by driver")
        notify("application_received", f"{d} uploaded a {doc_type} document (pending review)", d.company)
        msg = "Uploaded! Your carrier will review and approve it."
    items = []
    for label, dt in DQF_CHECKLIST:
        st = _dqf_item_status(d, dt)
        items.append({"label_name": label, "cls": st["cls"], "label": st["label"]})
    return render(request, "operations/driver_upload.html",
                  {"d": d, "items": items, "msg": msg,
                   "doc_types": ComplianceDocument.DOC_TYPE_CHOICES})


# ================= Billing / Invoicing (Core) =================
from .models import Invoice, Payment

INV_STATUS_CLASS = {"paid": "c-green", "partial": "c-blue", "unpaid": "c-gray"}


@require_section("billing")
@login_required
def app_billing(request):
    cs = _companies(request)
    invoices = Invoice.objects.filter(company__in=cs).select_related("company", "broker", "load").prefetch_related("payments")
    start = request.GET.get("start", ""); end = request.GET.get("end", "")
    def parse(d):
        try: return _dt.date.fromisoformat(d)
        except ValueError: return None
    sd, ed = parse(start), parse(end)
    if sd: invoices = invoices.filter(issue_date__gte=sd)
    if ed: invoices = invoices.filter(issue_date__lte=ed)
    rows, t_inv, t_paid, t_out = [], 0, 0, 0
    for inv in invoices:
        rows.append({"o": inv, "cls": INV_STATUS_CLASS.get(inv.status, "c-gray"),
                     "overdue": inv.is_overdue})
        t_inv += inv.total; t_paid += inv.paid; t_out += inv.balance
    # A/R aging snapshot over ALL open invoices in scope (independent of the date filter)
    today = _dt.date.today()
    aging = {"current": 0, "d1_30": 0, "d31_60": 0, "d61_90": 0, "d90": 0}
    for inv in Invoice.objects.filter(company__in=cs).prefetch_related("payments"):
        bal = inv.balance
        if bal <= 0:
            continue
        ref = inv.due_date or inv.issue_date
        days = (today - ref).days if ref else 0
        if days <= 0: aging["current"] += bal
        elif days <= 30: aging["d1_30"] += bal
        elif days <= 60: aging["d31_60"] += bal
        elif days <= 90: aging["d61_90"] += bal
        else: aging["d90"] += bal
    return render(request, "operations/app_billing.html", {
        "rows": rows, "t_inv": t_inv, "t_paid": t_paid, "t_out": t_out,
        "start": start, "end": end, "count": len(rows), "aging": aging,
    })


@require_section("billing")
@login_required
def invoice_detail(request, pk):
    inv = _get(Invoice, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_invoice_detail.html", {
        "inv": inv, "cls": INV_STATUS_CLASS.get(inv.status, "c-gray"),
        "methods": Payment.METHOD_CHOICES,
    })


@login_required
def invoice_create(request):
    cs = _companies_all(request)
    if request.method == "POST":
        company = _get(Company, pk=request.POST.get("company"), pk__in=cs.values_list("pk", flat=True))
        def num(v):
            try: return float(str(v).replace("$", "").replace(",", "") or 0)
            except ValueError: return 0
        def date(v):
            try: return _dt.date.fromisoformat(v)
            except (ValueError, TypeError): return None
        inv = Invoice.objects.create(
            company=company,
            invoice_number=request.POST.get("invoice_number", "").strip(),
            broker_id=request.POST.get("broker") or None,
            bill_to_name=request.POST.get("bill_to_name", "").strip(),
            load_id=request.POST.get("load") or None,
            issue_date=date(request.POST.get("issue_date")) or _dt.date.today(),
            due_date=date(request.POST.get("due_date")),
            subtotal=num(request.POST.get("subtotal")),
            discount=num(request.POST.get("discount")),
            tax=num(request.POST.get("tax")),
            notes=request.POST.get("notes", "").strip(),
        )
        ActivityLog.objects.create(category="billing", user=request.user, company=company,
            text=f"Created invoice {inv.invoice_number} (${inv.total}) for {inv.bill_to}")
        return redirect("invoice_detail", pk=inv.id)
    return render(request, "operations/app_invoice_form.html", {
        "companies": cs, "brokers": Broker.objects.all(),
        "loads": Load.objects.filter(company__in=cs)[:200], "today": _dt.date.today().isoformat(),
    })


@login_required
def payment_add(request, pk):
    inv = _get(Invoice, pk=pk, company__in=_companies_all(request))
    if request.method == "POST":
        def num(v):
            try: return float(str(v).replace("$", "").replace(",", "") or 0)
            except ValueError: return 0
        amt = num(request.POST.get("amount"))
        if amt > 0:
            try:
                pdate = _dt.date.fromisoformat(request.POST.get("payment_date"))
            except (ValueError, TypeError):
                pdate = _dt.date.today()
            Payment.objects.create(
                invoice=inv, amount=amt, method=request.POST.get("method", "check"),
                transaction_id=request.POST.get("transaction_id", "").strip(),
                payment_date=pdate, note=request.POST.get("note", "").strip())
            ActivityLog.objects.create(category="billing", user=request.user, company=inv.company,
                text=f"Recorded ${amt} payment on invoice {inv.invoice_number} "
                     f"(balance ${inv.balance})")
    return redirect("invoice_detail", pk=inv.id)


@require_section("billing")
@login_required
def invoice_print(request, pk):
    inv = _get(Invoice, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/invoice_print.html", {"inv": inv})


# ================= PDF generation + emailing (1099) =================
import io as _io2
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage


_LOGO_B64 = None
def _logo_data_uri(company=None):
    """Return a logo as a base64 data URI for PDFs. Uses the company's own
    uploaded logo when present, otherwise the shared Fleetline logo."""
    import base64, os
    if company is not None and getattr(company, "logo", None):
        try:
            company.logo.open("rb")
            data = company.logo.read()
            company.logo.close()
            ext = company.logo.name.lower().rsplit(".", 1)[-1]
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            return f"data:image/{mime};base64," + base64.b64encode(data).decode()
        except Exception:
            pass
    global _LOGO_B64
    if _LOGO_B64 is None:
        from django.conf import settings as _s
        path = os.path.join(_s.BASE_DIR, "operations", "static", "logo.png")
        try:
            with open(path, "rb") as f:
                _LOGO_B64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()
        except OSError:
            _LOGO_B64 = ""
    return _LOGO_B64


def _render_pdf(template, context):
    context = {**context, "logo_uri": _logo_data_uri(context.get("company"))}
    from xhtml2pdf import pisa
    html = render_to_string(template, context)
    buf = _io2.BytesIO()
    pisa.CreatePDF(html, dest=buf)
    return buf.getvalue()


def _1099_context(request, driver_id, year):
    companies = _companies_all(request)
    d = _get(Driver, pk=driver_id, company__in=companies)
    paid = Settlement.objects.filter(driver=d, period_end__year=year).aggregate(s=Sum("gross_pay"))["s"] or 0
    return {"d": d, "company": d.company, "paid": f"{paid:,.2f}", "year": year}


@login_required
def generate_1099_pdf(request, driver_id):
    year = int(request.GET.get("year", _dt.date.today().year))
    ctx = _1099_context(request, driver_id, year)
    pdf = _render_pdf("operations/pdf_1099.html", ctx)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="1099-{ctx["d"].last_name}-{year}.pdf"'
    return resp


@login_required
def email_1099(request, driver_id):
    year = int(request.GET.get("year", _dt.date.today().year))
    ctx = _1099_context(request, driver_id, year)
    if request.method == "POST":
        to = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip() or \
            f"Please find attached the 1099-NEC summary for {ctx['d']} ({year})."
        if not getattr(settings, "EMAIL_HOST", ""):
            _messages.error(request, "Email isn't set up yet. Add your email settings in Railway, then try again.")
            return redirect(f"/tax/1099/{driver_id}/?year={year}")
        if not to:
            _messages.error(request, "Please enter a recipient email address.")
            return redirect(f"/tax/1099/{driver_id}/?year={year}")
        pdf = _render_pdf("operations/pdf_1099.html", ctx)
        msg = EmailMessage(
            subject=f"1099-NEC — {ctx['d']} ({year})",
            body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to])
        msg.attach(f"1099-{ctx['d'].last_name}-{year}.pdf", pdf, "application/pdf")
        try:
            msg.send(fail_silently=False)
            ActivityLog.objects.create(category="billing", user=request.user, company=ctx["d"].company,
                text=f"Emailed 1099 for {ctx['d']} to {to}")
            _messages.success(request, f"1099 emailed to {to}.")
        except Exception as e:
            _messages.error(request, f"Could not send email: {e}")
    return redirect(f"/tax/1099/{driver_id}/?year={year}")


# ================= Vehicle report (PDF / print / email) =================
def _vehicle_report_context(request, pk):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    records = v.maintenance.all()
    today = _dt.date.today()
    total_all = sum((r.total for r in records), 0)
    total_year = sum((r.total for r in records if r.date and r.date.year == today.year), 0)
    return {"v": v, "records": records, "total_all": f"{total_all:,.2f}",
            "total_year": f"{total_year:,.2f}", "service": _service_chip(v),
            "insp": _exp_chip(v.inspection_expiry), "reg": _exp_chip(v.registration_expiry),
            "today": today}


@login_required
def vehicle_report_pdf(request, pk):
    ctx = _vehicle_report_context(request, pk)
    pdf = _render_pdf("operations/pdf_vehicle.html", ctx)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="unit-{ctx["v"].unit_number}-report.pdf"'
    return resp


@login_required
def email_vehicle_report(request, pk):
    ctx = _vehicle_report_context(request, pk)
    v = ctx["v"]
    if request.method == "POST":
        to = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip() or \
            f"Attached is the vehicle report for Unit {v.unit_number}."
        if not getattr(settings, "EMAIL_HOST", ""):
            _messages.error(request, "Email isn't set up yet. Add your email settings in Railway, then try again.")
            return redirect("app_vehicle_detail", pk=v.id)
        if not to:
            _messages.error(request, "Please enter a recipient email address.")
            return redirect("app_vehicle_detail", pk=v.id)
        pdf = _render_pdf("operations/pdf_vehicle.html", ctx)
        msg = EmailMessage(subject=f"Vehicle report — Unit {v.unit_number}",
                           body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to])
        msg.attach(f"unit-{v.unit_number}-report.pdf", pdf, "application/pdf")
        try:
            msg.send(fail_silently=False)
            ActivityLog.objects.create(category="maintenance", user=request.user, company=v.company,
                text=f"Emailed Unit {v.unit_number} report to {to}")
            _messages.success(request, f"Vehicle report emailed to {to}.")
        except Exception as e:
            _messages.error(request, f"Could not send email: {e}")
    return redirect("app_vehicle_detail", pk=v.id)


# ================= Fleet-wide maintenance report =================
def _fleet_maint_data(request):
    cs = _companies(request)
    records = MaintenanceRecord.objects.filter(company__in=cs).select_related("vehicle", "company")
    start = request.GET.get("start", ""); end = request.GET.get("end", "")
    def parse(d):
        try: return _dt.date.fromisoformat(d)
        except ValueError: return None
    sd, ed = parse(start), parse(end)
    if sd: records = records.filter(date__gte=sd)
    if ed: records = records.filter(date__lte=ed)
    today = _dt.date.today()
    # per-vehicle rollup
    per = {}
    for r in records:
        v = r.vehicle
        d = per.setdefault(v.id, {"unit": v.unit_number, "company": v.company.name,
                                  "count": 0, "parts": 0, "labor": 0, "total": 0})
        d["count"] += 1; d["parts"] += r.parts_cost or 0
        d["labor"] += r.labor_cost or 0; d["total"] += r.total
    per_vehicle = sorted(per.values(), key=lambda x: x["total"], reverse=True)
    # monthly rollup
    months = {}
    for r in records:
        if r.date:
            months[r.date.strftime("%Y-%m")] = months.get(r.date.strftime("%Y-%m"), 0) + r.total
    monthly = [{"month": _dt.datetime.strptime(k, "%Y-%m").strftime("%b %Y"), "total": t}
               for k, t in sorted(months.items(), reverse=True)]
    grand = sum((r.total for r in records), 0)
    parts_total = sum((r.parts_cost or 0 for r in records), 0)
    labor_total = sum((r.labor_cost or 0 for r in records), 0)
    year_total = sum((r.total for r in records if r.date and r.date.year == today.year), 0)
    month_total = sum((r.total for r in records if r.date and r.date.year == today.year
                       and r.date.month == today.month), 0)
    return {"per_vehicle": per_vehicle, "monthly": monthly, "grand": grand,
            "parts_total": parts_total, "labor_total": labor_total,
            "year_total": year_total, "month_total": month_total,
            "count": records.count(), "start": start, "end": end,
            "company_obj": cs.first() if cs.count() == 1 else None, "today": today}


@login_required
def fleet_maintenance(request):
    return render(request, "operations/app_maintenance.html", _fleet_maint_data(request))


@login_required
def fleet_maintenance_pdf(request):
    data = _fleet_maint_data(request)
    data["grand"] = f"{data['grand']:,.2f}"; data["parts_total"] = f"{data['parts_total']:,.2f}"
    data["labor_total"] = f"{data['labor_total']:,.2f}"
    pdf = _render_pdf("operations/pdf_maintenance.html", data)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'inline; filename="fleet-maintenance-report.pdf"'
    return resp


# ================= Factoring aging =================
def _factoring_aging_data(request):
    cs = _companies(request)
    # Outstanding with the factor = submitted / advanced / reserve released (not unpaid, not closed)
    open_states = ["submitted", "advanced", "reserve_released"]
    loads = Load.objects.filter(company__in=cs, payment_status__in=open_states).select_related("company", "broker")
    today = _dt.date.today()
    aging = {"current": 0, "d1_30": 0, "d31_60": 0, "d61_90": 0, "d90": 0}
    rows = []
    total = 0
    for l in loads:
        ref_date = l.delivery_date or l.pickup_date
        days = (today - ref_date).days if ref_date else 0
        rate = l.rate or 0
        total += rate
        if days <= 0: bucket = "current"
        elif days <= 30: bucket = "d1_30"
        elif days <= 60: bucket = "d31_60"
        elif days <= 90: bucket = "d61_90"
        else: bucket = "d90"
        aging[bucket] += rate
        rows.append({"ref": l.reference, "customer": l.broker.name if l.broker else (l.customer or "—"),
                     "company": l.company.name, "factor": l.company.factor,
                     "delivered": ref_date, "days": days if ref_date else None,
                     "rate": rate, "status": l.get_payment_status_display(),
                     "cls": "c-red" if days > 90 else ("c-warn" if days > 30 else "c-green")})
    rows.sort(key=lambda r: (r["days"] is not None, r["days"] or 0), reverse=True)
    return {"aging": aging, "rows": rows, "total": total, "count": len(rows),
            "company_obj": cs.first() if cs.count() == 1 else None, "today": today}


@login_required
def factoring_aging(request):
    return render(request, "operations/app_factoring_aging.html", _factoring_aging_data(request))


@login_required
def factoring_aging_pdf(request):
    data = _factoring_aging_data(request)
    data["total"] = f"{data['total']:,.2f}"
    pdf = _render_pdf("operations/pdf_factoring.html", data)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'inline; filename="factoring-aging.pdf"'
    return resp


# ================= Create load from a Rate Confirmation =================
import re as _re, os as _os, json as _json


def _ratecon_text(uploaded):
    """Extract text from an uploaded rate-con PDF (text-based PDFs)."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(uploaded)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        return ""


def _ratecon_ai(text):
    """High-accuracy extraction via Anthropic API, only if a key is configured."""
    key = _os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or not text.strip():
        return None
    try:
        import urllib.request
        prompt = ("Extract fields from this freight rate confirmation. Respond with ONLY a JSON "
                  "object, no prose, with keys: broker_name, mc_number, reference, origin, "
                  "destination, pickup_date (YYYY-MM-DD or ''), delivery_date (YYYY-MM-DD or ''), "
                  "rate (number). Use '' if unknown.\n\n" + text[:6000])
        model = _os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
        body = _json.dumps({"model": model, "max_tokens": 400,
                            "messages": [{"role": "user", "content": prompt}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
            headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"})
        resp = _json.loads(urllib.request.urlopen(req, timeout=30).read())
        raw = resp["content"][0]["text"].strip()
        raw = raw[raw.find("{"):raw.rfind("}") + 1]
        return _json.loads(raw)
    except Exception:
        return None


def _ratecon_heuristic(text):
    d = {"broker_name": "", "mc_number": "", "reference": "", "origin": "",
         "destination": "", "pickup_date": "", "delivery_date": "", "rate": ""}
    m = _re.search(r"MC[#\s:.]*?(\d{4,8})", text, _re.I)
    if m: d["mc_number"] = m.group(1)
    amts = [float(x.replace(",", "")) for x in _re.findall(r"\$\s*([\d,]+\.\d{2})", text)]
    if amts: d["rate"] = max(amts)
    m = _re.search(r"(?:load|order|pro|ref\w*|bol)\s*[#:]?\s*([A-Z0-9\-]*\d[A-Z0-9\-]*)", text, _re.I)
    if m: d["reference"] = m.group(1)
    dates = _re.findall(r"(\d{1,2}/\d{1,2}/\d{2,4})", text)
    def iso(x):
        for f in ("%m/%d/%Y", "%m/%d/%y"):
            try: return _dt.datetime.strptime(x, f).date().isoformat()
            except ValueError: continue
        return ""
    if dates: d["pickup_date"] = iso(dates[0])
    if len(dates) > 1: d["delivery_date"] = iso(dates[1])
    cities = _re.findall(r"([A-Z][A-Za-z\.\s]{1,24},\s*[A-Z]{2})\b", text)
    if cities: d["origin"] = cities[0].strip()
    if len(cities) > 1: d["destination"] = cities[1].strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines: d["broker_name"] = lines[0][:120]
    return d


@require_section("dispatch")
@login_required
def load_from_ratecon(request):
    companies = _companies_all(request)
    if request.method == "POST" and request.FILES.get("ratecon"):
        f = request.FILES["ratecon"]
        text = _ratecon_text(f)
        data = _ratecon_ai(text) or _ratecon_heuristic(text)
        company = _get(Company, pk=request.POST.get("company"),
                       pk__in=companies.values_list("pk", flat=True))
        # auto-add / link broker
        broker = None
        mc = str(data.get("mc_number") or "").strip()
        bname = str(data.get("broker_name") or "").strip()
        if mc:
            broker = Broker.objects.filter(mc_number=mc).first()
        if not broker and bname:
            broker = Broker.objects.filter(name__iexact=bname).first()
        if not broker and (mc or bname):
            broker = Broker.objects.create(name=bname or f"MC {mc}", mc_number=mc)
        def rate():
            try: return float(str(data.get("rate") or 0).replace("$", "").replace(",", "") or 0)
            except ValueError: return 0
        def date(v):
            try: return _dt.date.fromisoformat(v)
            except (ValueError, TypeError): return None
        f.seek(0)
        load = Load.objects.create(
            company=company, reference=str(data.get("reference") or "")[:40],
            customer=bname[:120], broker=broker,
            origin=str(data.get("origin") or "")[:120], destination=str(data.get("destination") or "")[:120],
            pickup_date=date(data.get("pickup_date")), delivery_date=date(data.get("delivery_date")),
            rate=rate(), rate_confirmation=f, status="booked")
        ActivityLog.objects.create(category="load", user=request.user, company=company,
            text=f"Created load {load.reference or load.id} from rate confirmation"
                 + (f" · added broker {broker.name}" if broker else ""))
        _messages.success(request, "Load created from the rate confirmation. Please review and correct any fields below.")
        return redirect(f"/admin/operations/load/{load.id}/change/")
    return render(request, "operations/app_ratecon.html",
                  {"companies": companies, "ai_on": bool(_os.environ.get("ANTHROPIC_API_KEY"))})


# ================= Portfolio: all-companies command center =================
@require_section("portfolio")
@login_required
def portfolio(request):
    companies = _companies_all(request)
    today = _dt.date.today()
    soon = today + _dt.timedelta(days=30)
    cards = []
    tot = {"loads": 0, "drivers": 0, "vehicles": 0, "ar": 0, "alerts": 0, "factoring": 0}
    for c in companies:
        active_loads = Load.objects.filter(company=c).exclude(payment_status="closed")\
            .exclude(status="delivered").count()
        drivers = Driver.objects.filter(company=c).count()
        vehicles = Vehicle.objects.filter(company=c).count()
        ar = sum((inv.balance for inv in Invoice.objects.filter(company=c).prefetch_related("payments")), 0)
        # compliance alerts: driver CDL/medical + vehicle inspection/registration expiring within 30d
        alerts = 0
        for d in Driver.objects.filter(company=c):
            for dt_ in (d.cdl_expiry, d.medical_expiry):
                if dt_ and dt_ <= soon:
                    alerts += 1
        for v in Vehicle.objects.filter(company=c):
            for dt_ in (v.inspection_expiry, v.registration_expiry, v.next_service_date):
                if dt_ and dt_ <= soon:
                    alerts += 1
        factoring = Load.objects.filter(company=c, payment_status__in=["submitted", "advanced", "reserve_released"])\
            .aggregate(s=Sum("rate"))["s"] or 0
        cards.append({"c": c, "loads": active_loads, "drivers": drivers, "vehicles": vehicles,
                      "ar": ar, "alerts": alerts, "factoring": factoring})
        tot["loads"] += active_loads; tot["drivers"] += drivers; tot["vehicles"] += vehicles
        tot["ar"] += ar; tot["alerts"] += alerts; tot["factoring"] += factoring
    return render(request, "operations/app_portfolio.html", {"cards": cards, "tot": tot, "count": companies.count()})


# ================= Team: edit member, reset password, invite =================
from django.contrib.auth.tokens import default_token_generator as _tokgen
from django.utils.http import urlsafe_base64_encode as _uidenc
from django.utils.encoding import force_bytes as _fbytes
from django.urls import reverse as _reverse


@require_section("team")
@login_required
def team_edit(request, pk):
    if not _is_manager(request.user):
        _messages.error(request, "Only managers can edit team members.")
        return redirect("app_team")
    m = _get(_User, pk=pk)
    if m.is_superuser and not request.user.is_superuser:
        _messages.error(request, "Only the owner can edit the owner account.")
        return redirect("app_team")
    prof, _ = Profile.objects.get_or_create(user=m)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "details":
            m.first_name = request.POST.get("first_name", "").strip()
            m.last_name = request.POST.get("last_name", "").strip()
            m.email = request.POST.get("email", "").strip()
            m.save()
            prof.phone = request.POST.get("phone", "").strip()
            role = request.POST.get("role", prof.role)
            if role == "admin" and not request.user.is_superuser:
                role = prof.role  # only the owner can grant Admin
            prof.role = role
            prof.save()
            prof.companies.set(request.POST.getlist("companies"))
            _apply_role(m, role)
            ActivityLog.objects.create(category="team", user=request.user,
                text=f"Updated team member {m.get_full_name() or m.username}")
            _messages.success(request, "Details saved.")
        elif action == "setpw":
            pw = request.POST.get("password", "").strip()
            if len(pw) < 6:
                _messages.error(request, "Password must be at least 6 characters.")
            else:
                m.set_password(pw); m.save()
                ActivityLog.objects.create(category="team", user=request.user,
                    text=f"Reset password for {m.username}")
                _messages.success(request, f"Password updated for {m.username}. Share it with them securely.")
        return redirect("team_edit", pk=pk)
    return render(request, "operations/app_team_edit.html", {
        "m": m, "prof": prof, "roles": Profile.ROLE_CHOICES,
        "all_companies": _companies_all(request),
        "member_company_ids": list(prof.companies.values_list("id", flat=True)),
        "can_assign_admin": request.user.is_superuser,
    })


@require_section("team")
@login_required
def team_send_reset(request, pk):
    if not _is_manager(request.user):
        return redirect("app_team")
    m = _get(_User, pk=pk)
    uid = _uidenc(_fbytes(m.pk))
    token = _tokgen.make_token(m)
    link = request.build_absolute_uri(
        _reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))
    emailed = False
    if getattr(settings, "EMAIL_HOST", "") and m.email:
        try:
            from django.core.mail import send_mail
            send_mail(
                "Set up your Trucking Compliance Services login",
                f"Hi {m.first_name or m.username},\n\n"
                f"Use this link to set your password:\n{link}\n\n"
                f"If you didn't expect this, you can ignore it.",
                settings.DEFAULT_FROM_EMAIL, [m.email], fail_silently=False)
            emailed = True
        except Exception as e:
            _messages.error(request, f"Could not send email: {e}")
    if emailed:
        ActivityLog.objects.create(category="team", user=request.user,
            text=f"Emailed password-setup link to {m.email}")
        _messages.success(request, f"Password-setup email sent to {m.email}.")
    else:
        _messages.info(request, f"Email isn't set up (or no address on file), so copy this "
                                f"link and send it to {m.get_full_name() or m.username}: {link}")
    return redirect("team_edit", pk=pk)


# ================= Per-truck profit / loss report =================
def _per_truck_data(request):
    from .models import MaintenanceRecord
    cs = _companies(request)
    start = _parse_date(request.GET.get("start", ""))
    end = _parse_date(request.GET.get("end", ""))
    groups = []
    gt = {"rev": 0, "fuel": 0, "maint": 0, "net": 0, "loads": 0}
    for c in cs.order_by("name"):
        trucks = []
        for v in Vehicle.objects.filter(company=c).order_by("unit_number"):
            lq = Load.objects.filter(vehicle=v)
            fq = FuelTransaction.objects.filter(vehicle=v)
            mq = MaintenanceRecord.objects.filter(vehicle=v)
            if start:
                lq = lq.filter(pickup_date__gte=start); fq = fq.filter(date__gte=start); mq = mq.filter(date__gte=start)
            if end:
                lq = lq.filter(pickup_date__lte=end); fq = fq.filter(date__lte=end); mq = mq.filter(date__lte=end)
            rev = lq.aggregate(s=Sum("rate"))["s"] or 0
            fuel = fq.aggregate(s=Sum("amount"))["s"] or 0
            maint = sum((r.parts_cost or 0) + (r.labor_cost or 0) for r in mq)
            loads = lq.count()
            net = rev - fuel - maint
            trucks.append({"v": v, "rev": rev, "fuel": fuel, "maint": maint, "net": net, "loads": loads})
            gt["rev"] += rev; gt["fuel"] += fuel; gt["maint"] += maint; gt["net"] += net; gt["loads"] += loads
        if trucks:
            groups.append({"company": c, "trucks": trucks})
    # letterhead company (only when a single company is in scope)
    company = cs.first() if cs.count() == 1 else None
    return {"groups": groups, "gt": gt, "company": company,
            "start": request.GET.get("start", ""), "end": request.GET.get("end", "")}


@require_section("reports")
@login_required
def per_truck_pnl(request):
    return render(request, "operations/pnl_truck.html", _per_truck_data(request))


@require_section("reports")
@login_required
def per_truck_pnl_pdf(request):
    from django.http import HttpResponse
    data = _per_truck_data(request)
    pdf = _render_pdf("operations/pnl_truck_pdf.html", data)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'attachment; filename="per-truck-profit-loss.pdf"'
    return resp


# ================= Branded per-company portal login =================
def portal_login(request, slug=None):
    from django.contrib.auth import authenticate, login as _login
    company = Company.objects.filter(slug=slug).first() if slug else None
    error = ""
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST.get("username", "").strip(),
                            password=request.POST.get("password", ""))
        if user is not None and user.is_active:
            _login(request, user)
            # land the user inside this company if they're allowed to see it
            if company is not None:
                allowed = user.is_superuser or \
                    (hasattr(user, "profile") and user.profile.companies.filter(pk=company.pk).exists())
                if allowed:
                    request.session["active_company"] = str(company.pk)
            return redirect("dashboard")
        error = "Wrong username or password."
    return render(request, "registration/portal_login.html",
                  {"company": company, "error": error, "slug": slug or ""})


# ================= Tasks =================
from .models import Task, PerformanceNote


@require_section("dashboard")
@login_required
def tasks_page(request):
    cs = _companies(request)
    tasks = Task.objects.filter(company__in=cs).select_related(
        "assignee", "driver", "vehicle", "load", "company")
    # non-managers see only tasks assigned to them
    if not _is_manager(request.user):
        tasks = tasks.filter(assignee=request.user)
    status = request.GET.get("status", "active")
    if status == "active":
        tasks = tasks.exclude(status__in=["done", "cancelled"])
    elif status and status != "all":
        tasks = tasks.filter(status=status)
    rows = list(tasks)
    # data for the "new task" form
    members = _User.objects.filter(is_active=True, is_staff=True).order_by("first_name", "username") \
        if _is_manager(request.user) else _User.objects.filter(pk=request.user.pk)
    drivers = Driver.objects.filter(company__in=cs).order_by("first_name")
    vehicles = Vehicle.objects.filter(company__in=cs).order_by("unit_number")
    return render(request, "operations/tasks.html", {
        "tasks": rows, "status": status, "can_assign": _is_manager(request.user),
        "members": members, "drivers": drivers, "vehicles": vehicles,
        "companies": cs, "priorities": Task.PRIORITY, "statuses": Task.STATUS,
        "open_count": Task.objects.filter(company__in=cs).exclude(status__in=["done", "cancelled"])
            .filter(**({} if _is_manager(request.user) else {"assignee": request.user})).count(),
    })


@login_required
def task_create(request):
    if request.method != "POST":
        return redirect("tasks_page")
    if not _is_manager(request.user):
        # non-managers can only self-assign
        pass
    cs = _companies(request)
    company = cs.filter(pk=request.POST.get("company")).first() or cs.first()
    if not company:
        _messages.error(request, "Pick a company first."); return redirect("tasks_page")
    t = Task(company=company, title=request.POST.get("title", "").strip(),
             details=request.POST.get("details", "").strip(),
             priority=request.POST.get("priority", "normal"),
             created_by=request.user)
    if not t.title:
        _messages.error(request, "Task needs a title."); return redirect("tasks_page")
    aid = request.POST.get("assignee")
    if aid:
        t.assignee = _User.objects.filter(pk=aid).first()
    if not _is_manager(request.user):
        t.assignee = request.user
    did = request.POST.get("driver")
    if did:
        t.driver = Driver.objects.filter(pk=did, company__in=cs).first()
    vid = request.POST.get("vehicle")
    if vid:
        t.vehicle = Vehicle.objects.filter(pk=vid, company__in=cs).first()
    due = _parse_date(request.POST.get("due_date", ""))
    if due:
        t.due_date = due
    t.save()
    ActivityLog.objects.create(company=company, user=request.user, category="task",
                               text=f"Task assigned: {t.title}")
    _messages.success(request, "Task created.")
    return redirect("tasks_page")


@login_required
def task_status(request, pk):
    if request.method != "POST":
        return redirect("tasks_page")
    t = _get(Task, pk=pk, company__in=_companies(request))
    # only a manager or the assignee can change it
    if not (_is_manager(request.user) or t.assignee_id == request.user.id):
        _messages.error(request, "You can't change that task."); return redirect("tasks_page")
    new = request.POST.get("status")
    if new in dict(Task.STATUS):
        t.status = new
        if new == "done" and not t.completed_at:
            from django.utils import timezone
            t.completed_at = timezone.now()
        t.save()
    return redirect("tasks_page")


# ================= Performance (people + trucks) =================
@require_section("reports")
@login_required
def performance_page(request):
    cs = _companies(request)
    start = _parse_date(request.GET.get("start", ""))
    end = _parse_date(request.GET.get("end", ""))

    def date_filter(qs, field):
        if start: qs = qs.filter(**{f"{field}__gte": start})
        if end: qs = qs.filter(**{f"{field}__lte": end})
        return qs

    # Drivers: loads, revenue, tasks done, avg rating
    drivers = []
    for d in Driver.objects.filter(company__in=cs).order_by("first_name"):
        lq = date_filter(Load.objects.filter(driver=d), "pickup_date")
        ratings = [n.rating for n in d.perf_notes.all() if n.rating]
        drivers.append({
            "d": d, "loads": lq.count(),
            "revenue": lq.aggregate(s=Sum("rate"))["s"] or 0,
            "notes": d.perf_notes.count(),
            "avg": round(sum(ratings) / len(ratings), 1) if ratings else None,
        })
    # Trucks: loads, revenue, fuel
    trucks = []
    for v in Vehicle.objects.filter(company__in=cs).order_by("unit_number"):
        lq = date_filter(Load.objects.filter(vehicle=v), "pickup_date")
        fq = date_filter(FuelTransaction.objects.filter(vehicle=v), "date")
        ratings = [n.rating for n in v.perf_notes.all() if n.rating]
        trucks.append({
            "v": v, "loads": lq.count(),
            "revenue": lq.aggregate(s=Sum("rate"))["s"] or 0,
            "fuel": fq.aggregate(s=Sum("amount"))["s"] or 0,
            "notes": v.perf_notes.count(),
            "avg": round(sum(ratings) / len(ratings), 1) if ratings else None,
        })
    # Team members: tasks assigned/done
    members = []
    if _is_manager(request.user):
        for u in _User.objects.filter(is_staff=True, is_active=True).order_by("first_name", "username"):
            tq = Task.objects.filter(assignee=u, company__in=cs)
            done = tq.filter(status="done").count()
            members.append({"u": u, "assigned": tq.count(), "done": done,
                            "open": tq.exclude(status__in=["done", "cancelled"]).count()})
    return render(request, "operations/performance.html", {
        "drivers": drivers, "trucks": trucks, "members": members,
        "start": request.GET.get("start", ""), "end": request.GET.get("end", ""),
    })


@login_required
def perf_note_add(request):
    if request.method != "POST":
        return redirect("performance_page")
    cs = _companies(request)
    subject_type = request.POST.get("subject_type")  # driver | vehicle | member
    subject_id = request.POST.get("subject_id")
    note = request.POST.get("note", "").strip()
    rating = request.POST.get("rating") or None
    if not note:
        _messages.error(request, "Write a note first."); return redirect("performance_page")
    pn = PerformanceNote(note=note, author=request.user,
                         rating=int(rating) if rating else None)
    if subject_type == "driver":
        d = Driver.objects.filter(pk=subject_id, company__in=cs).first()
        if d: pn.driver = d; pn.company = d.company
    elif subject_type == "vehicle":
        v = Vehicle.objects.filter(pk=subject_id, company__in=cs).first()
        if v: pn.vehicle = v; pn.company = v.company
    elif subject_type == "member":
        m = _User.objects.filter(pk=subject_id).first()
        if m: pn.member = m; pn.company = cs.first()
    if not pn.company_id:
        _messages.error(request, "Could not attach that note."); return redirect("performance_page")
    pn.save()
    _messages.success(request, "Performance note added.")
    return redirect(request.POST.get("next", "/app/performance/"))


# ================= Performance detail (clickable person / truck) =================
@require_section("reports")
@login_required
def performance_detail(request, kind, pk):
    cs = _companies(request)
    ctx = {"kind": kind}
    if kind == "driver":
        subj = _get(Driver, pk=pk, company__in=cs)
        lq = Load.objects.filter(driver=subj)
        ctx.update({"subj": subj, "name": str(subj),
                    "loads": lq.count(), "revenue": lq.aggregate(s=Sum("rate"))["s"] or 0})
        notes = subj.perf_notes.all()
    elif kind == "vehicle":
        subj = _get(Vehicle, pk=pk, company__in=cs)
        lq = Load.objects.filter(vehicle=subj)
        fq = FuelTransaction.objects.filter(vehicle=subj)
        ctx.update({"subj": subj, "name": f"Unit {subj.unit_number}",
                    "loads": lq.count(), "revenue": lq.aggregate(s=Sum("rate"))["s"] or 0,
                    "fuel": fq.aggregate(s=Sum("amount"))["s"] or 0})
        notes = subj.perf_notes.all()
    else:  # member
        subj = _get(_User, pk=pk)
        tq = Task.objects.filter(assignee=subj, company__in=cs)
        ctx.update({"subj": subj, "name": subj.get_full_name() or subj.username,
                    "assigned": tq.count(), "done": tq.filter(status="done").count(),
                    "open": tq.exclude(status__in=["done", "cancelled"]).count()})
        notes = subj.perf_notes.all()
    ratings = [n.rating for n in notes if n.rating]
    ctx["avg"] = round(sum(ratings) / len(ratings), 1) if ratings else None
    ctx["notes"] = notes
    return render(request, "operations/performance_detail.html", ctx)


# ================= Internal team communication (TeamNote) =================
from .models import TeamNote


def _notify_team_note(request, note):
    """Email the team (background) that a new note was posted. Never blocks."""
    if not getattr(settings, "EMAIL_HOST", ""):
        return
    # team members on this company, excluding the author, who have an email
    recipients = list(_User.objects.filter(
        is_staff=True, is_active=True, profile__companies=note.company)
        .exclude(pk=note.author_id).exclude(email="")
        .values_list("email", flat=True).distinct())
    if not recipients:
        return
    import threading
    author = note.author.get_full_name() if note.author else "A teammate"
    subj = f"[{note.company.name}] New team note — {note.subject_label}"
    body = (f"{author} posted a note ({note.subject_label}):\n\n{note.body}\n\n"
            f"Open the portal to reply.")

    def _send():
        try:
            from django.core.mail import send_mail
            send_mail(subj, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()


@require_section("dashboard")
@login_required
def team_board(request):
    cs = _companies(request)
    notes = TeamNote.objects.filter(company__in=cs, broker__isnull=True,
                                    load__isnull=True, driver__isnull=True) \
        .select_related("author", "company")
    return render(request, "operations/team_board.html", {
        "notes": notes, "companies": cs, "scope": "board"})


@login_required
def team_note_add(request):
    if request.method != "POST":
        return redirect("team_board")
    cs = _companies(request)
    body = request.POST.get("body", "").strip()
    if not body:
        _messages.error(request, "Write something first.")
        return redirect(request.POST.get("next", "/app/board/"))
    company = cs.filter(pk=request.POST.get("company")).first() or cs.first()
    note = TeamNote(company=company, author=request.user, body=body)
    # optional attachment
    for field, model in (("broker", Broker), ("load", Load), ("driver", Driver)):
        val = request.POST.get(field)
        if val:
            obj = model.objects.filter(pk=val, company__in=cs).first() if field != "broker" \
                else Broker.objects.filter(pk=val).first()
            if obj:
                setattr(note, field, obj)
    note.save()
    _notify_team_note(request, note)
    _messages.success(request, "Note posted.")
    return redirect(request.POST.get("next", "/app/board/"))


@login_required
def team_note_pin(request, pk):
    if request.method == "POST":
        n = _get(TeamNote, pk=pk, company__in=_companies(request))
        n.pinned = not n.pinned
        n.save()
    return redirect(request.POST.get("next", "/app/board/"))


# ================= Driver weekly settlements / pay =================
@require_section("reports")
@login_required
def driver_pay(request):
    cs = _companies(request)
    settlements = Settlement.objects.filter(company__in=cs).select_related("driver", "company")
    show = request.GET.get("show", "all")
    if show == "unpaid":
        settlements = settlements.filter(paid=False)
    elif show == "paid":
        settlements = settlements.filter(paid=True)
    rows = list(settlements.order_by("-period_end"))
    drivers = Driver.objects.filter(company__in=cs).order_by("first_name")
    # default the "new" week to the last 7 days
    today = _dt.date.today()
    monday = today - _dt.timedelta(days=today.weekday())
    return render(request, "operations/driver_pay.html", {
        "rows": rows, "drivers": drivers, "show": show,
        "week_start": (monday - _dt.timedelta(days=7)).isoformat(),
        "week_end": (monday - _dt.timedelta(days=1)).isoformat(),
        "companies": cs,
    })


@require_section("reports")
@login_required
def driver_pay_new(request):
    if request.method != "POST":
        return redirect("driver_pay")
    cs = _companies(request)
    d = Driver.objects.filter(pk=request.POST.get("driver"), company__in=cs).first()
    if not d:
        _messages.error(request, "Pick a driver."); return redirect("driver_pay")
    ps = _parse_date(request.POST.get("period_start")) or _dt.date.today()
    pe = _parse_date(request.POST.get("period_end")) or _dt.date.today()
    basis = request.POST.get("pay_basis", "weekly")
    if basis == "daily":
        day = _parse_date(request.POST.get("day_date", "")) or _parse_date(request.POST.get("period_start", "")) or _dt.date.today()
        ps = pe = day
    s = Settlement.objects.create(
        company=d.company, driver=d, period_start=ps, period_end=pe, pay_basis=basis,
        gross_pay=_num(request.POST.get("gross_pay", "0")),
        deductions=_num(request.POST.get("deductions", "0")),
        notes=request.POST.get("notes", "").strip())
    # AUTO-attach for weekly/daily (loads picked up OR delivered in the range).
    # Per-load starts empty — you add the exact loads/round-trips yourself.
    if basis != "per_load":
        from django.db.models import Q as _Q
        auto_loads = Load.objects.filter(driver=d, settlement__isnull=True).filter(
            _Q(pickup_date__gte=ps, pickup_date__lte=pe) |
            _Q(delivery_date__gte=ps, delivery_date__lte=pe))
        auto_loads.update(settlement=s)
    # if no gross was typed, suggest it. Percentage drivers get their % of the
    # loads' rates; everyone else gets the full loads total (you can edit either way).
    if not s.gross_pay:
        loads_total = float(s.loads.aggregate(x=Sum("rate"))["x"] or 0)
        if d.pay_type == "percentage" and d.pay_rate:
            s.gross_pay = round(loads_total * float(d.pay_rate) / 100, 2)
        else:
            s.gross_pay = loads_total
        s.save()
    return redirect("driver_pay_detail", pk=s.id)


@require_section("reports")
@login_required
def driver_pay_detail(request, pk):
    cs = _companies(request)
    s = _get(Settlement, pk=pk, company__in=cs)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "edit":
            s.gross_pay = _num(request.POST.get("gross_pay", "0"))
            s.deductions = _num(request.POST.get("deductions", "0"))
            s.extra_reimbursement = _num(request.POST.get("extra_reimbursement", "0"))
            s.notes = request.POST.get("notes", "").strip()
            s.save(); _messages.success(request, "Updated.")
        elif action == "use_loads_total":
            s.gross_pay = s.loads.aggregate(x=Sum("rate"))["x"] or 0
            s.save(); _messages.success(request, "Gross pay set from the attached loads.")
        elif action == "use_percent":
            pct = _num(request.POST.get("percent", "0"))
            total = float(s.loads.aggregate(x=Sum("rate"))["x"] or 0)
            s.gross_pay = round(total * pct / 100, 2)
            s.save(); _messages.success(request, f"Gross set to {pct:.0f}% of loads (${s.gross_pay}).")
        elif action == "add_load":
            lid = request.POST.get("load_id", "").strip()
            if not lid:
                _messages.error(request, "Pick a load from the list first.")
                return redirect("driver_pay_detail", pk=pk)
            l = Load.objects.filter(pk=lid, company__in=cs, driver=s.driver).first()
            if l:
                l.settlement = s; l.save(); _messages.success(request, f"Added load {l.reference}.")
            else:
                _messages.error(request, "That load could not be added.")
        elif action == "delete":
            # free the attached loads, then remove the settlement
            s.loads.update(settlement=None)
            s.delete()
            _messages.success(request, "Settlement deleted.")
            return redirect("driver_pay")
        elif action == "toggle_hide_amounts":
            s.hide_load_amounts = not s.hide_load_amounts
            s.save()
            _messages.success(request, "Load amounts hidden." if s.hide_load_amounts else "Load amounts shown.")
        elif action == "new_load":
            ref = request.POST.get("nl_ref", "").strip()
            rate = _num(request.POST.get("nl_rate", "0"))
            if not ref and not rate:
                _messages.error(request, "Enter at least a load # or a rate.")
                return redirect("driver_pay_detail", pk=pk)
            nl = Load.objects.create(
                company=s.company, driver=s.driver, settlement=s,
                reference=ref or "MANUAL",
                origin=request.POST.get("nl_origin", "").strip(),
                destination=request.POST.get("nl_destination", "").strip(),
                rate=rate,
                miles=int(_num(request.POST.get("nl_miles", "0"))),
                deadhead_miles=int(_num(request.POST.get("nl_deadhead", "0"))),
                pickup_date=_parse_date(request.POST.get("nl_pickup", "")) or None,
                status="delivered")
            _messages.success(request, f"Added load {nl.reference}.")
            return redirect("driver_pay_detail", pk=pk)
        elif action == "remove_load":
            l = s.loads.filter(pk=request.POST.get("load_id")).first()
            if l:
                l.settlement = None; l.save(); _messages.success(request, f"Removed load {l.reference}.")
        elif action == "pay":
            s.paid = True
            s.paid_date = _parse_date(request.POST.get("paid_date")) or _dt.date.today()
            s.payment_method = request.POST.get("payment_method", "").strip()
            s.payment_reference = request.POST.get("payment_reference", "").strip()
            s.save()
            ActivityLog.objects.create(company=s.company, user=request.user, category="pay",
                text=f"Paid {s.driver} ${s.net_pay} ref {s.payment_reference}")
            _messages.success(request, "Marked as paid.")
        elif action == "unpay":
            s.paid = False; s.save()
        return redirect("driver_pay_detail", pk=pk)
    oop = Expense.objects.filter(driver=s.driver, out_of_pocket=True,
                                 date__gte=s.period_start, date__lte=s.period_end)
    settle_loads = s.loads.select_related("broker", "vehicle").order_by("pickup_date")
    loads_total = settle_loads.aggregate(x=Sum("rate"))["x"] or 0
    # loads for this driver not yet on any settlement (available to add)
    addable = Load.objects.filter(driver=s.driver, settlement__isnull=True).order_by("-pickup_date")[:50]
    return render(request, "operations/driver_pay_detail.html",
                  {"s": s, "oop": oop, "company": s.company,
                   "settle_loads": settle_loads, "loads_total": loads_total, "addable": addable,
                   **_driver_pay_totals(s.driver)})


@require_section("reports")
@login_required
def driver_pay_pdf(request, pk):
    from django.http import HttpResponse
    s = _get(Settlement, pk=pk, company__in=_companies(request))
    oop = Expense.objects.filter(driver=s.driver, out_of_pocket=True,
                                 date__gte=s.period_start, date__lte=s.period_end)
    _sl = s.loads.order_by("pickup_date")
    _mi = _sl.aggregate(a=Sum("miles"), b=Sum("deadhead_miles"), r=Sum("rate"))
    pdf = _render_pdf("operations/driver_pay_pdf.html", {"s": s, "oop": oop, "company": s.company,
                       "settle_loads": _sl,
                       "total_loaded": _mi["a"] or 0, "total_deadhead": _mi["b"] or 0,
                       "total_miles": (_mi["a"] or 0) + (_mi["b"] or 0),
                       "loads_total": _mi["r"] or 0})
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="settlement-{s.driver}-{s.period_end}.pdf"'
    return resp


@require_section("reports")
@login_required
def driver_pay_email(request, pk):
    s = _get(Settlement, pk=pk, company__in=_companies(request))
    if not s.driver.email:
        _messages.error(request, f"{s.driver} has no email on file. Add one on the driver's record.")
        return redirect("driver_pay_detail", pk=pk)
    if not getattr(settings, "EMAIL_HOST", ""):
        _messages.error(request, "Email isn't connected yet.")
        return redirect("driver_pay_detail", pk=pk)
    oop = Expense.objects.filter(driver=s.driver, out_of_pocket=True,
                                 date__gte=s.period_start, date__lte=s.period_end)
    _sl = s.loads.order_by("pickup_date")
    _mi = _sl.aggregate(a=Sum("miles"), b=Sum("deadhead_miles"), r=Sum("rate"))
    pdf = _render_pdf("operations/driver_pay_pdf.html", {"s": s, "oop": oop, "company": s.company,
                       "settle_loads": _sl,
                       "total_loaded": _mi["a"] or 0, "total_deadhead": _mi["b"] or 0,
                       "total_miles": (_mi["a"] or 0) + (_mi["b"] or 0),
                       "loads_total": _mi["r"] or 0})
    try:
        from django.core.mail import EmailMessage
        msg = EmailMessage(
            subject=f"Your settlement — {s.period_start} to {s.period_end}",
            body=f"Hi {s.driver.first_name},\n\nAttached is your pay statement for "
                 f"{s.period_start} to {s.period_end}. Net pay: ${s.net_pay:.2f}."
                 + (f"\nPaid via {s.payment_method} ref {s.payment_reference}." if s.paid else ""),
            from_email=settings.DEFAULT_FROM_EMAIL, to=[s.driver.email])
        msg.attach(f"settlement-{s.period_end}.pdf", pdf, "application/pdf")
        msg.send(fail_silently=False)
        _messages.success(request, f"Statement emailed to {s.driver.email}.")
    except Exception as e:
        _messages.error(request, f"Could not send: {e}")
    return redirect("driver_pay_detail", pk=pk)


# ================= Single-truck P&L detail (drill-down) =================
def _truck_detail_data(request, pk):
    from .models import MaintenanceRecord
    cs = _companies(request)
    v = _get(Vehicle, pk=pk, company__in=cs)
    start = _parse_date(request.GET.get("start", ""))
    end = _parse_date(request.GET.get("end", ""))
    loads = Load.objects.filter(vehicle=v).select_related("broker", "driver").order_by("-pickup_date")
    fuel = FuelTransaction.objects.filter(vehicle=v).order_by("-date")
    maint = MaintenanceRecord.objects.filter(vehicle=v).order_by("-date")
    exp = Expense.objects.filter(vehicle=v).order_by("-date")
    if start:
        loads = loads.filter(pickup_date__gte=start); fuel = fuel.filter(date__gte=start)
        maint = maint.filter(date__gte=start); exp = exp.filter(date__gte=start)
    if end:
        loads = loads.filter(pickup_date__lte=end); fuel = fuel.filter(date__lte=end)
        maint = maint.filter(date__lte=end); exp = exp.filter(date__lte=end)
    revenue = loads.aggregate(s=Sum("rate"))["s"] or 0
    fuel_total = fuel.aggregate(s=Sum("amount"))["s"] or 0
    maint_total = sum((r.parts_cost or 0) + (r.labor_cost or 0) for r in maint)
    exp_total = exp.aggregate(s=Sum("amount"))["s"] or 0
    # rental/lease estimate for leased or rented trucks
    rent_total = 0
    active_contract = v.contracts.filter(active=True).first()
    if v.ownership in ("leased", "rented") and active_contract:
        miles_in_range = (loads.aggregate(m=Sum("miles"))["m"] or 0) + \
                         (loads.aggregate(m=Sum("deadhead_miles"))["m"] or 0)
        rs = start or (loads.order_by("pickup_date").first().pickup_date if loads.exists() else None)
        re_ = end or _dt.date.today()
        if rs:
            rent_total = active_contract.estimated_cost(rs, re_, miles_in_range)
    net = float(revenue) - float(fuel_total) - float(maint_total) - float(exp_total) - float(rent_total)
    return {
        "v": v, "company": v.company, "loads": loads, "fuel": fuel, "maint": maint, "exp": exp,
        "revenue": revenue, "fuel_total": fuel_total, "maint_total": maint_total,
        "exp_total": exp_total, "rent_total": rent_total, "active_contract": active_contract,
        "net": net,
        "start": request.GET.get("start", ""), "end": request.GET.get("end", ""),
        "loads_count": loads.count(), "fuel_gal": fuel.aggregate(s=Sum("gallons"))["s"] or 0,
    }


@require_section("reports")
@login_required
def truck_detail(request, pk):
    return render(request, "operations/truck_detail.html", _truck_detail_data(request, pk))


@require_section("reports")
@login_required
def truck_detail_pdf(request, pk):
    from django.http import HttpResponse
    data = _truck_detail_data(request, pk)
    pdf = _render_pdf("operations/truck_detail_pdf.html", data)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="truck-{data["v"].unit_number}-pnl.pdf"'
    return resp


# ================= Single-driver detail (loads + pay + expenses) =================
def _driver_report_data(request, pk):
    cs = _companies(request)
    d = _get(Driver, pk=pk, company__in=cs)
    start = _parse_date(request.GET.get("start", ""))
    end = _parse_date(request.GET.get("end", ""))
    loads = Load.objects.filter(driver=d).select_related("broker", "vehicle").order_by("-pickup_date")
    setts = Settlement.objects.filter(driver=d).order_by("-period_end")
    exp = Expense.objects.filter(driver=d).order_by("-date")
    if start:
        loads = loads.filter(pickup_date__gte=start); setts = setts.filter(period_end__gte=start); exp = exp.filter(date__gte=start)
    if end:
        loads = loads.filter(pickup_date__lte=end); setts = setts.filter(period_start__lte=end); exp = exp.filter(date__lte=end)
    revenue = loads.aggregate(s=Sum("rate"))["s"] or 0
    total_paid = sum(s.net_pay for s in setts if s.paid)
    total_unpaid = sum(s.net_pay for s in setts if not s.paid)
    oop_total = exp.filter(out_of_pocket=True).aggregate(s=Sum("amount"))["s"] or 0
    return {
        "d": d, "company": d.company, "loads": loads, "setts": setts, "exp": exp,
        "revenue": revenue, "loads_count": loads.count(),
        "total_paid": total_paid, "total_unpaid": total_unpaid, "oop_total": oop_total,
        "start": request.GET.get("start", ""), "end": request.GET.get("end", ""),
        **_driver_pay_totals(d),
    }


@require_section("reports")
@login_required
def driver_report(request, pk):
    return render(request, "operations/driver_report.html", _driver_report_data(request, pk))


@require_section("reports")
@login_required
def driver_report_pdf(request, pk):
    from django.http import HttpResponse
    data = _driver_report_data(request, pk)
    pdf = _render_pdf("operations/driver_report_pdf.html", data)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="driver-{data["d"]}-report.pdf"'
    return resp


def _driver_pay_totals(driver):
    """How much this driver has been PAID: this month, this year, all-time,
    plus a per-month breakdown for the current year. Uses paid settlements."""
    today = _dt.date.today()
    paid = Settlement.objects.filter(driver=driver, paid=True)
    month_total = year_total = all_total = 0
    monthly = {m: 0 for m in range(1, 13)}
    for s in paid:
        net = float(s.net_pay)
        all_total += net
        d = s.paid_date or s.period_end
        if d and d.year == today.year:
            year_total += net
            monthly[d.month] = monthly.get(d.month, 0) + net
            if d.month == today.month:
                month_total += net
    months = [(_dt.date(today.year, m, 1).strftime("%b"), monthly[m]) for m in range(1, 13) if monthly[m]]
    return {"pay_month": month_total, "pay_year": year_total, "pay_all": all_total,
            "pay_months": months, "pay_year_label": today.year}


# ================= Load import from CSV / spreadsheet (e.g. Amazon Relay) =================
@require_section("dispatch")
@login_required
def load_import(request):
    cs = _companies(request)
    active = _active(request)
    default_company = cs.filter(pk=active).first() if active and active != "all" else cs.first()
    context = {"companies": cs, "default_company": default_company, "drivers":
               Driver.objects.filter(company__in=cs).order_by("first_name"),
               "vehicles": Vehicle.objects.filter(company__in=cs).order_by("unit_number")}

    if request.method == "POST":
        import csv, io
        f = request.FILES.get("file")
        if not f:
            _messages.error(request, "Choose a CSV file first.")
            return render(request, "operations/load_import.html", context)
        company = cs.filter(pk=request.POST.get("company")).first() or default_company
        # optional defaults applied to every imported load
        def_driver = Driver.objects.filter(pk=request.POST.get("driver"), company__in=cs).first()
        def_vehicle = Vehicle.objects.filter(pk=request.POST.get("vehicle"), company__in=cs).first()
        try:
            raw = f.read().decode("utf-8-sig", errors="ignore")
            reader = csv.reader(io.StringIO(raw))
            rows = [r for r in reader if any(c.strip() for c in r)]
        except Exception as e:
            _messages.error(request, f"Could not read the file: {e}")
            return render(request, "operations/load_import.html", context)
        if len(rows) < 2:
            _messages.error(request, "The file has no data rows.")
            return render(request, "operations/load_import.html", context)
        header = rows[0]
        # column detection — needle-priority (works with Amazon Relay & most TMS exports)
        col = {
            "ref": _find(header, "trip", "vrid", "load id", "load", "reference", "ref", "order", "tour"),
            "origin": _find(header, "origin", "pickup", "pick up", "first stop", "ship from"),
            "destination": _find(header, "destination", "dest", "drop off", "dropoff", "delivery", "deliver", "consignee", "last stop", "final stop", "ship to"),
            "pickup_date": _find(header, "pickup date", "start date", "pickup", "ready", "depart"),
            "delivery_date": _find(header, "delivery date", "end date", "drop date", "arrive", "due"),
            "rate": _find(header, "rate", "line haul", "linehaul", "block pay", "block rate", "total pay",
                          "gross pay", "amount", "pay", "revenue", "total", "cost", "price", "charge"),
            "miles": _find(header, "loaded mile", "miles", "distance", "mileage"),
            "deadhead": _find(header, "deadhead", "empty mile", "dh mile", "dh"),
            "customer": _find(header, "customer", "broker", "shipper", "account"),
        }
        # collect every "stop" column (Stop 1, Stop 2, Stop A, Location 1...) for multi-stop / LTL
        stop_cols = [i for i, h in enumerate(header)
                     if h and ("stop" in h.lower() or "location" in h.lower())]
        if col["ref"] is None and col["origin"] is None and col["rate"] is None:
            _messages.error(request, "Couldn't recognize the columns. Make sure the first row has headers like Trip/Load ID, Origin, Destination, Rate.")
            return render(request, "operations/load_import.html", context)

        def val(row, key):
            i = col.get(key)
            return row[i].strip() if (i is not None and i < len(row)) else ""

        created = skipped = 0
        for row in rows[1:]:
            ref = val(row, "ref")
            origin = val(row, "origin")
            rate = _num(val(row, "rate"))
            # gather all stop columns (multi-stop / LTL) in order
            stops_list = [row[i].strip() for i in stop_cols if i < len(row) and row[i].strip()]
            stops_text = "\n".join(stops_list)
            # if there was no explicit origin/destination, use first/last stop
            if not origin and stops_list:
                origin = stops_list[0]
            dest = val(row, "destination")
            if not dest and len(stops_list) > 1:
                dest = stops_list[-1]
            if not ref and not origin and not rate and not stops_list:
                continue
            # skip duplicates: same company + reference (if a reference exists)
            if ref and Load.objects.filter(company=company, reference=ref).exists():
                skipped += 1
                continue
            Load.objects.create(
                company=company,
                reference=ref or "RELAY",
                customer=val(row, "customer"),
                origin=origin,
                destination=dest,
                stops=stops_text,
                pickup_date=_parse_date(val(row, "pickup_date")) or None,
                delivery_date=_parse_date(val(row, "delivery_date")) or None,
                rate=rate,
                miles=int(_num(val(row, "miles"))),
                deadhead_miles=int(_num(val(row, "deadhead"))),
                driver=def_driver, vehicle=def_vehicle,
                status="booked")
            created += 1
        msg = f"Imported {created} load(s)."
        if skipped:
            msg += f" Skipped {skipped} already in the system (same reference)."
        _messages.success(request, msg)
        return redirect("app_loads")

    return render(request, "operations/load_import.html", context)


@require_section("vehicles")
@login_required
def vehicle_doc_upload(request, pk):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    if request.method == "POST" and request.FILES.get("file"):
        try:
            # make sure the media subfolder exists (belt-and-suspenders for volumes)
            import os
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "vehicle_docs"), exist_ok=True)
            VehicleDocument.objects.create(
                company=v.company, vehicle=v,
                doc_type=request.POST.get("doc_type", "other"),
                custom_type=request.POST.get("custom_type", "").strip(),
                title=request.POST.get("title", "").strip(),
                file=request.FILES["file"],
                expiry_date=_parse_date(request.POST.get("expiry_date", "")) or None,
                notes=request.POST.get("notes", "").strip())
            _messages.success(request, "Document uploaded.")
        except Exception as e:
            _messages.error(request, f"Could not save the document: {e}")
    else:
        _messages.error(request, "Choose a file to upload.")
    return redirect("app_vehicle_detail", pk=pk)


@require_section("vehicles")
@login_required
def vehicle_doc_delete(request, pk, doc_id):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    if request.method == "POST":
        d = v.documents.filter(pk=doc_id).first()
        if d:
            d.delete(); _messages.success(request, "Document removed.")
    return redirect("app_vehicle_detail", pk=pk)


@require_section("dispatch")
@login_required
def load_doc_upload(request, pk):
    """Quick upload of BOL / POD / Rate con right from the load page (no admin)."""
    l = _get(Load, pk=pk, company__in=_companies_all(request))
    if request.method == "POST":
        field = request.POST.get("which")
        f = request.FILES.get("file")
        allowed = {"bill_of_lading", "proof_of_delivery", "rate_confirmation"}
        if field in allowed and f:
            try:
                import os
                sub = {"bill_of_lading": "loads/bol", "proof_of_delivery": "loads/pod",
                       "rate_confirmation": "loads/ratecon"}[field]
                os.makedirs(os.path.join(settings.MEDIA_ROOT, sub), exist_ok=True)
                setattr(l, field, f); l.save()
                _messages.success(request, "Document uploaded.")
            except Exception as e:
                _messages.error(request, f"Could not save the document: {e}")
        else:
            _messages.error(request, "Pick a document type and a file.")
    return redirect("app_load_detail", pk=pk)


# ================= FMCSA carrier lookup (QCMobile API) =================
def _fmcsa_key():
    import os
    return os.environ.get("FMCSA_WEBKEY", "").strip()


def _fmcsa_fetch(dot=None, mc=None):
    """Look up a carrier on FMCSA QCMobile. Returns (data_dict, error_str)."""
    import json
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
    key = _fmcsa_key()
    if not key:
        return None, "No FMCSA key set. Add FMCSA_WEBKEY in your Railway settings first."
    base = "https://mobile.fmcsa.dot.gov/qc/services/carriers"
    if dot:
        url = f"{base}/{dot}?webKey={key}"
    elif mc:
        url = f"{base}/docket-number/{mc}?webKey={key}"
    else:
        return None, "Enter a DOT or MC number."
    try:
        with urlopen(url, timeout=15) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        return None, f"FMCSA returned an error ({e.code}). Check the number and try again."
    except (URLError, TimeoutError) as e:
        return None, f"Could not reach FMCSA: {e}. Try again in a moment."
    except Exception as e:
        return None, f"Lookup failed: {e}"
    # QCMobile wraps carrier data under "content" -> "carrier" (or a list for MC)
    content = payload.get("content")
    if isinstance(content, list):
        content = content[0] if content else None
    if not content:
        return None, "No carrier found for that number."
    carrier = content.get("carrier", content) if isinstance(content, dict) else None
    if not carrier:
        return None, "No carrier data returned."
    return carrier, None


@require_section("dispatch")
@login_required
def fmcsa_lookup(request):
    """AJAX-style: return FMCSA carrier data as JSON for the add-company form."""
    from django.http import JsonResponse
    dot = (request.GET.get("dot") or "").strip()
    mc = (request.GET.get("mc") or "").strip()
    carrier, err = _fmcsa_fetch(dot=dot or None, mc=mc or None)
    if err:
        return JsonResponse({"ok": False, "error": err})

    def g(*keys):
        for k in keys:
            v = carrier.get(k)
            if v not in (None, "", "NONE"):
                return v
        return ""
    # build a single address line
    addr_parts = [str(g("phyStreet")), str(g("phyCity")), str(g("phyState")), str(g("phyZipcode"))]
    address = ", ".join(p for p in addr_parts if p and p != "None")
    data = {
        "name": g("legalName", "dbaName"),
        "dba": g("dbaName"),
        "dot_number": str(g("dotNumber")),
        "mc_number": str(g("docketNumber") or mc),
        "address": address,
        "phone": g("phone", "telephone"),
        "safety_rating": g("safetyRating") or "Not rated",
        "fmcsa_status": g("allowedToOperate") == "Y" and "Allowed to operate" or g("statusCode") or "",
        "power_units": g("totalPowerUnits") or g("powerUnits") or "",
        "drivers": g("totalDrivers") or g("driverTotal") or "",
    }
    return JsonResponse({"ok": True, "data": data})


@login_required
def company_new(request):
    """Add a company, optionally auto-filled from FMCSA by DOT/MC number."""
    if not request.user.is_superuser:
        return redirect("dashboard")
    if request.method == "POST":
        import datetime as _d
        name = request.POST.get("name", "").strip()
        if not name:
            _messages.error(request, "Company name is required.")
            return redirect("company_new")
        c = Company.objects.create(
            name=name,
            dot_number=request.POST.get("dot_number", "").strip(),
            mc_number=request.POST.get("mc_number", "").strip(),
            address=request.POST.get("address", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            email=request.POST.get("email", "").strip(),
            safety_rating=request.POST.get("safety_rating", "").strip(),
            fmcsa_status=request.POST.get("fmcsa_status", "").strip(),
            power_units=(int(_num(request.POST.get("power_units", "0"))) or None),
            fmcsa_updated=_d.date.today() if request.POST.get("safety_rating") else None,
        )
        # give the creating superuser access + set as active
        _messages.success(request, f"Company '{c.name}' added.")
        return redirect("dashboard")
    return render(request, "operations/company_new.html", {"has_key": bool(_fmcsa_key())})


@login_required
def company_access(request):
    """Owner-only: create a login for a specific company. The new user sees ONLY
    that company's data (trucks, accounting, expenses, documents) with its logo."""
    if not request.user.is_superuser:
        return redirect("dashboard")
    companies = Company.objects.filter(active=True).order_by("name")
    if request.method == "POST":
        company = companies.filter(pk=request.POST.get("company")).first()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        role = request.POST.get("role", "admin")
        first = request.POST.get("first_name", "").strip()
        email = request.POST.get("email", "").strip()
        if not company:
            _messages.error(request, "Pick a company.")
        elif not username or not password:
            _messages.error(request, "Username and password are required.")
        elif len(password) < 8:
            _messages.error(request, "Use a password of at least 8 characters.")
        elif _User.objects.filter(username__iexact=username).exists():
            _messages.error(request, "That username is already taken.")
        else:
            u = _User.objects.create_user(username=username, password=password,
                                          first_name=first, email=email)
            prof, _ = Profile.objects.get_or_create(user=u, defaults={"role": role})
            prof.role = role
            prof.save()
            prof.companies.set([company])          # ONLY this company
            _apply_role(u, role)                    # permissions for their role
            _messages.success(request,
                f"Login created for {company.name}. Username: {username}. "
                f"They can sign in at /c/{company.slug}/ and will see only their own data.")
            return redirect("company_access")
    # list existing per-company logins (non-superusers with a single company)
    logins = []
    for u in _User.objects.filter(is_superuser=False).select_related("profile"):
        try:
            prof = u.profile
        except Profile.DoesNotExist:
            continue
        comps = list(prof.companies.all())
        if len(comps) == 1:
            logins.append({"u": u, "company": comps[0], "role": prof.get_role_display()})
    return render(request, "operations/company_access.html",
                  {"companies": companies, "roles": Profile.ROLE_CHOICES, "logins": logins})

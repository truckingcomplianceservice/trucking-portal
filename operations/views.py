"""Views: P&L, protected media, public hiring form, compliance dashboard, hiring links."""
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.static import serve
from django.conf import settings
from .models import (Company, Load, Expense, Settlement, Driver, Vehicle, Applicant,
                     ComplianceDocument, Broker, FuelTransaction, notify)


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


@login_required
def app_loads(request):
    cs = _companies(request)
    loads = Load.objects.filter(company__in=cs).select_related("company", "driver")
    rows = [{"o": l, "sc": STATUS_CLASS.get(l.status, "c-gray"),
             "pc": PAY_CLASS.get(l.payment_status, "c-gray")} for l in loads]
    return render(request, "operations/app_loads.html", {"rows": rows})


@login_required
def app_load_detail(request, pk):
    l = _get(Load, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_load_detail.html",
                  {"l": l, "sc": STATUS_CLASS.get(l.status, "c-gray"),
                   "pc": PAY_CLASS.get(l.payment_status, "c-gray")})


@login_required
def app_drivers(request):
    cs = _companies(request)
    drivers = Driver.objects.filter(company__in=cs).select_related("company")
    rows = [{"o": d, "cdl": _exp_chip(d.cdl_expiry), "med": _exp_chip(d.medical_expiry),
             "dqf": _dqf_overall(d),
             "initials": (d.first_name[:1] + d.last_name[:1]).upper()} for d in drivers]
    return render(request, "operations/app_drivers.html", {"rows": rows})


@login_required
def app_driver_detail(request, pk):
    d = _get(Driver, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_driver_detail.html",
                  {"d": d, "cdl": _exp_chip(d.cdl_expiry), "med": _exp_chip(d.medical_expiry)})


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


@login_required
def app_vehicles(request):
    cs = _companies(request)
    vehicles = Vehicle.objects.filter(company__in=cs).select_related("company")
    rows = [{"o": v, "insp": _exp_chip(v.inspection_expiry),
             "reg": _exp_chip(v.registration_expiry), "service": _service_chip(v)} for v in vehicles]
    return render(request, "operations/app_vehicles.html", {"rows": rows})


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
    return render(request, "operations/app_vehicle_detail.html",
                  {"v": v, "insp": _exp_chip(v.inspection_expiry),
                   "reg": _exp_chip(v.registration_expiry), "service": _service_chip(v),
                   "records": records, "total_all": total_all, "total_year": total_year,
                   "total_month": total_month, "monthly": monthly, "today": today.isoformat()})


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


@login_required
def app_compliance(request):
    items = _expiring_items(_companies(request))
    overdue = [i for i in items if i["days"] < 0]
    soon = [i for i in items if 0 <= i["days"] <= 30]
    ok = [i for i in items if i["days"] > 30]
    return render(request, "operations/app_compliance.html",
                  {"overdue": overdue, "soon": soon, "ok": ok, "count": len(overdue) + len(soon)})


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
    expenses = Expense.objects.filter(company__in=cs).select_related("company")[:8]
    settlements = Settlement.objects.filter(company__in=cs).select_related("driver", "company")[:8]
    totals = {"rev": tr, "exp": te, "wag": tw, "net": tr - te - tw}
    return render(request, "operations/app_accounting.html",
                  {"rows": rows, "totals": totals, "expenses": expenses, "settlements": settlements})


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
                   "start": start, "end": end, "qs": qs, "count": txns.count()})


def _find(header, *needles):
    for i, h in enumerate(header):
        hl = h.strip().lower()
        if any(n in hl for n in needles):
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


@login_required
def fuel_import(request):
    companies = _companies_all(request)
    ctx = {"companies": companies, "step": "upload"}
    if request.method == "POST":
        stage = request.POST.get("stage")
        # STEP 1 -> read file, guess columns, show mapping
        if stage == "preview" and request.FILES.get("file"):
            raw = request.FILES["file"].read().decode("utf-8", errors="ignore")
            rows = list(_csv.reader(_io.StringIO(raw)))
            if rows:
                header = rows[0]
                guess = {
                    "date": _find(header, "date"),
                    "amount": _find(header, "amount", "amt", "total", "net", "cost", "charge",
                                    "invoice", "purchase", "sale", "spent", "paid", "value", "$"),
                    "gallons": _find(header, "gallon", "qty", "quantity", "volume", "units"),
                    "location": _find(header, "merchant", "location", "site", "city", "station", "vendor"),
                    "card": _find(header, "card"),
                    "unit": _find(header, "unit", "vehicle", "truck", "asset"),
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
            created, skipped = 0, 0
            for row in rows[1:]:
                if not any(c.strip() for c in row):
                    continue
                def cell(key):
                    i = idx[key]
                    return row[i] if i is not None and i < len(row) else ""
                amount = _num(cell("amount")); gallons = _num(cell("gallons"))
                if amount == 0 and gallons == 0:
                    skipped += 1; continue
                vehicle = None; unit = cell("unit").strip()
                if unit:
                    vehicle = Vehicle.objects.filter(company=company, unit_number__iexact=unit).first()
                card = cell("card").strip()
                FuelTransaction.objects.create(
                    company=company, date=_parse_date(cell("date")), vehicle=vehicle,
                    card_last4=card[-4:] if card else "", location=cell("location").strip()[:160],
                    gallons=gallons, amount=amount, source="csv")
                created += 1
            ctx.update({"step": "done", "result": {"created": created, "skipped": skipped,
                        "company": company.name}})
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
    "accountant": ["expense", "settlement", "fueltransaction"],
    "billing": ["expense", "settlement", "load"],
    "driver": [],
}


def _apply_role(user, role):
    """Give a team member a Django group with permissions matching their role."""
    user.is_staff = True
    user.save()
    group, _ = Group.objects.get_or_create(name=f"role_{role}")
    perms = Permission.objects.filter(content_type__app_label="operations")
    models_allowed = ROLE_PERMS.get(role, [])
    if models_allowed != "ALL":
        keep = []
        for p in perms:
            model = p.content_type.model
            action = p.codename.split("_")[0]
            if model in models_allowed and action in ("add", "change", "view"):
                keep.append(p.id)
            elif action == "view":
                keep.append(p.id)  # everyone can view
        perms = Permission.objects.filter(id__in=keep)
    group.permissions.set(list(perms))
    user.groups.clear()
    user.groups.add(group)


def _is_manager(user):
    if user.is_superuser:
        return True
    try:
        return user.profile.role in ("admin", "manager")
    except Exception:
        return False


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
def _logo_data_uri():
    """Return the company logo as a base64 data URI for embedding in PDFs."""
    global _LOGO_B64
    if _LOGO_B64 is None:
        import base64, os
        from django.conf import settings as _s
        path = os.path.join(_s.BASE_DIR, "operations", "static", "logo.png")
        try:
            with open(path, "rb") as f:
                _LOGO_B64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()
        except OSError:
            _LOGO_B64 = ""
    return _LOGO_B64


def _render_pdf(template, context):
    context = {**context, "logo_uri": _logo_data_uri()}
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

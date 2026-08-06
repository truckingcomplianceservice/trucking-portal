"""Views: P&L, protected media, public hiring form, compliance dashboard, hiring links."""
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.static import serve
from django.conf import settings
from .models import (Company, Load, Expense, Settlement, Driver, Vehicle, Applicant,
                     ComplianceDocument, Broker, FuelTransaction)


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
from .models import ActivityLog


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
             "initials": (d.first_name[:1] + d.last_name[:1]).upper()} for d in drivers]
    return render(request, "operations/app_drivers.html", {"rows": rows})


@login_required
def app_driver_detail(request, pk):
    d = _get(Driver, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_driver_detail.html",
                  {"d": d, "cdl": _exp_chip(d.cdl_expiry), "med": _exp_chip(d.medical_expiry)})


@login_required
def app_vehicles(request):
    cs = _companies(request)
    vehicles = Vehicle.objects.filter(company__in=cs).select_related("company")
    rows = [{"o": v, "insp": _exp_chip(v.inspection_expiry)} for v in vehicles]
    return render(request, "operations/app_vehicles.html", {"rows": rows})


@login_required
def app_vehicle_detail(request, pk):
    v = _get(Vehicle, pk=pk, company__in=_companies_all(request))
    return render(request, "operations/app_vehicle_detail.html",
                  {"v": v, "insp": _exp_chip(v.inspection_expiry)})


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
    txns = FuelTransaction.objects.filter(company__in=cs).select_related("company", "vehicle", "driver")[:200]
    total_amt = FuelTransaction.objects.filter(company__in=cs).aggregate(s=Sum("amount"))["s"] or 0
    total_gal = FuelTransaction.objects.filter(company__in=cs).aggregate(s=Sum("gallons"))["s"] or 0
    return render(request, "operations/app_fuel.html",
                  {"txns": txns, "total_amt": total_amt, "total_gal": total_gal})


def _find(header, *needles):
    for i, h in enumerate(header):
        hl = h.strip().lower()
        if any(n in hl for n in needles):
            return i
    return None


def _num(val):
    if val is None:
        return 0
    v = str(val).replace("$", "").replace(",", "").strip()
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
    result = None
    if request.method == "POST" and request.FILES.get("file"):
        company_id = request.POST.get("company")
        company = _get(Company, pk=company_id, pk__in=companies.values_list("pk", flat=True))
        raw = request.FILES["file"].read().decode("utf-8", errors="ignore")
        reader = _csv.reader(_io.StringIO(raw))
        rows = list(reader)
        created, skipped = 0, 0
        if rows:
            header = rows[0]
            ix = {
                "date": _find(header, "date"),
                "amount": _find(header, "amount", "total", "net", "cost"),
                "gallons": _find(header, "gallon", "qty", "quantity", "units", "volume"),
                "location": _find(header, "merchant", "location", "site", "city", "station"),
                "card": _find(header, "card"),
                "unit": _find(header, "unit", "vehicle", "truck", "asset"),
                "driver": _find(header, "driver"),
            }
            def cell(row, key):
                i = ix[key]
                return row[i] if i is not None and i < len(row) else ""
            for row in rows[1:]:
                if not any(c.strip() for c in row):
                    continue
                amount = _num(cell(row, "amount"))
                gallons = _num(cell(row, "gallons"))
                if amount == 0 and gallons == 0:
                    skipped += 1
                    continue
                vehicle = None
                unit = cell(row, "unit").strip()
                if unit:
                    vehicle = Vehicle.objects.filter(company=company, unit_number__iexact=unit).first()
                card = cell(row, "card").strip()
                last4 = card[-4:] if card else ""
                FuelTransaction.objects.create(
                    company=company, date=_parse_date(cell(row, "date")),
                    vehicle=vehicle, card_last4=last4,
                    location=cell(row, "location").strip()[:160],
                    gallons=gallons, amount=amount, source="csv")
                created += 1
            result = {"created": created, "skipped": skipped, "company": company.name,
                      "matched": ", ".join(f"{k}={header[v]}" for k, v in ix.items() if v is not None)}
    return render(request, "operations/app_fuel_import.html",
                  {"companies": companies, "result": result})

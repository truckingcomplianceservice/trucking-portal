"""Views: P&L, protected media, public hiring form, compliance dashboard, hiring links."""
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.static import serve
from django.conf import settings
from .models import Company, Load, Expense, Settlement, Driver, Vehicle, Applicant, ComplianceDocument


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

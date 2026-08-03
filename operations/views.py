"""Phase 2 views: a P&L report per company, and protected serving of uploaded files."""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.views.static import serve
from django.conf import settings
from .models import Company, Load, Expense, Settlement


@login_required
def pnl_report(request):
    """Revenue - expenses - driver wages, per company, plus a combined total."""
    user = request.user
    companies = Company.objects.all()
    if not user.is_superuser:
        companies = companies.filter(pk__in=user.profile.companies.all())

    rows, tot_rev, tot_exp, tot_wag = [], 0, 0, 0
    for c in companies:
        rev = Load.objects.filter(company=c).aggregate(s=Sum("rate"))["s"] or 0
        exp = Expense.objects.filter(company=c).aggregate(s=Sum("amount"))["s"] or 0
        wag = sum(s.net_pay for s in Settlement.objects.filter(company=c))
        rows.append({"name": c.name, "mc": c.mc_number, "rev": rev, "exp": exp,
                     "wag": wag, "net": rev - exp - wag})
        tot_rev += rev; tot_exp += exp; tot_wag += wag

    totals = {"rev": tot_rev, "exp": tot_exp, "wag": tot_wag,
              "net": tot_rev - tot_exp - tot_wag}
    return render(request, "operations/pnl.html", {"rows": rows, "totals": totals})


@login_required
def protected_media(request, path):
    """Only logged-in users can open uploaded documents (BOL, POD, receipts)."""
    return serve(request, path, document_root=settings.MEDIA_ROOT)

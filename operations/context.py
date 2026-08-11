"""Makes the company switcher and nav available on every custom page."""
def nav(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    from .models import Company
    companies = Company.objects.all()
    if not request.user.is_superuser:
        companies = companies.filter(pk__in=request.user.profile.companies.all())
    return {"nav_companies": companies,
            "active_company_id": request.session.get("active_company", "all"),
            "multi_company": companies.count() > 1}

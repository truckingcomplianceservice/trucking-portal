"""Makes the company switcher and nav available on every custom page."""
def nav(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    from .models import Company
    companies = Company.objects.all()
    if not request.user.is_superuser:
        companies = companies.filter(pk__in=request.user.profile.companies.all())
    from .access import sections_for
    active_id = request.session.get("active_company", "all")
    active_company_obj = None
    if active_id and active_id != "all":
        active_company_obj = companies.filter(pk=active_id).first()
    elif companies.count() == 1:
        active_company_obj = companies.first()
    return {"nav_companies": companies,
            "active_company_obj": active_company_obj,
            "active_company_id": request.session.get("active_company", "all"),
            "multi_company": companies.count() > 1,
            "nav_allowed": sections_for(request.user)}

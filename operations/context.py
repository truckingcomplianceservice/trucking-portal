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
            "nav_allowed": sections_for(request.user),
            "TAWK_ID": __import__("os").environ.get("TAWK_ID", ""),
            "is_platform_owner": _is_platform_owner_ctx(request.user),
            "is_sales_team": getattr(getattr(request.user, "profile", None), "is_sales_team", False)}


def _is_platform_owner_ctx(user):
    """Same as views._is_platform_owner but usable in the context processor."""
    import os as _o
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    admins = _o.environ.get("PLATFORM_ADMINS", "")
    if admins and getattr(user, "email", ""):
        allowed = [a.strip().lower() for a in admins.split(",") if a.strip()]
        if user.email.strip().lower() in allowed:
            return True
    return False

"""Central role-based access map. One place to decide what each role can reach."""

SECTIONS = ["portfolio", "dashboard", "messages", "dispatch", "brokers", "drivers", "hiring",
            "vehicles", "fuel", "compliance", "billing", "accounting", "tax",
            "reports", "team"]

# Which sections each role may access. "ALL" = every section.
ROLE_SECTIONS = {
    "admin": "ALL",
    "manager": ["dashboard", "messages", "dispatch", "brokers", "drivers", "hiring", "vehicles",
                "fuel", "compliance", "billing", "accounting", "tax", "reports", "team"],
    "dispatcher": ["dashboard", "messages", "dispatch", "brokers", "drivers", "vehicles"],
    "compliance": ["dashboard", "messages", "drivers", "vehicles", "hiring", "compliance"],
    "safety": ["dashboard", "messages", "drivers", "vehicles", "compliance"],
    "accountant": ["dashboard", "messages", "fuel", "billing", "accounting", "tax", "reports"],
    "billing": ["dashboard", "messages", "billing", "accounting", "tax", "reports"],
    "driver": ["dashboard", "messages"],
}


def sections_for(user):
    """Set of sections this user may access."""
    if getattr(user, "is_superuser", False):
        return set(SECTIONS)
    try:
        role = user.profile.role
    except Exception:
        return {"dashboard"}
    allowed = ROLE_SECTIONS.get(role, ["dashboard"])
    result = set(SECTIONS) if allowed == "ALL" else set(allowed)
    result.discard("portfolio")   # all-companies money view is owner-only
    return result


def can(user, section):
    return section in sections_for(user)

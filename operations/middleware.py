"""Captures the current request user so activity logging can record who acted."""
import threading

_state = threading.local()


def get_current_user():
    return getattr(_state, "user", None)


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _state.user = getattr(request, "user", None)
        try:
            return self.get_response(request)
        finally:
            _state.user = None


# --- SEO: canonical-domain redirect --------------------------------------
# carrierconnect360.com (bare/apex) is the intended long-term canonical domain,
# but its DNS is not fully set up yet — it does not resolve. Until that's fixed,
# www.carrierconnect360.com is canonical instead, since it's the one that
# actually works. IMPORTANT: do not point CANONICAL_HOST at a domain that
# doesn't resolve — every alias host gets redirected here, so a broken
# canonical host takes the whole site down for anyone hitting an alias.
# Once the bare domain's DNS is confirmed working, flip these back:
#   CANONICAL_HOST = "carrierconnect360.com"
#   REDIRECT_ALIAS_HOSTS = {"www.carrierconnect360.com", "app.pure99inc.com"}
CANONICAL_HOST = "www.carrierconnect360.com"
REDIRECT_ALIAS_HOSTS = {"carrierconnect360.com", "app.pure99inc.com"}


class CanonicalDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        if host in REDIRECT_ALIAS_HOSTS:
            from django.http import HttpResponsePermanentRedirect
            target = f"https://{CANONICAL_HOST}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(target)
        return self.get_response(request)

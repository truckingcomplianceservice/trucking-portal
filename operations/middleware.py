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
# carrierconnect360.com is the canonical domain (set in <link rel="canonical">
# across the site). www.carrierconnect360.com and the legacy app.pure99inc.com
# serve the identical app, which splits SEO signal across three domains.
# This 301-redirects those aliases to the canonical domain, path and query
# string preserved. Railway's internal *.railway.app host (used for health
# checks) and localhost are deliberately excluded so deploys never break.
CANONICAL_HOST = "carrierconnect360.com"
REDIRECT_ALIAS_HOSTS = {"www.carrierconnect360.com", "app.pure99inc.com"}


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

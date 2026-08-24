"""
SMS sending via Twilio — activates only when Twilio credentials are configured.

To turn SMS on, set these environment variables (e.g. in Railway):
  TWILIO_ACCOUNT_SID   - your Twilio Account SID
  TWILIO_AUTH_TOKEN    - your Twilio Auth Token
  TWILIO_FROM_NUMBER   - your Twilio phone number, e.g. +15551234567

Until those are set, send_sms() safely does nothing and returns False, so the
rest of the app keeps working. No Twilio account = no crashes.

NOTE: business texting in the US also requires A2P 10DLC registration through
Twilio before carriers will deliver your messages reliably.
"""
import os
import re
import urllib.request
import urllib.parse
import urllib.error


def sms_enabled():
    return bool(os.environ.get("TWILIO_ACCOUNT_SID")
                and os.environ.get("TWILIO_AUTH_TOKEN")
                and os.environ.get("TWILIO_FROM_NUMBER"))


def _normalize(number):
    """Return an E.164-ish number. Assumes US (+1) if no country code given."""
    if not number:
        return ""
    n = number.strip()
    plus = n.startswith("+")
    digits = re.sub(r"[^0-9]", "", n)
    if plus:
        return "+" + digits
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    return "+" + digits if digits else ""


def send_sms(to_number, body):
    """Send one SMS. Returns True if sent, False otherwise. Never raises."""
    if not sms_enabled():
        return False
    to = _normalize(to_number)
    if not to:
        return False
    sid = os.environ["TWILIO_ACCOUNT_SID"]
    token = os.environ["TWILIO_AUTH_TOKEN"]
    from_number = os.environ["TWILIO_FROM_NUMBER"]
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data = urllib.parse.urlencode({
        "To": to, "From": from_number, "Body": body[:1500]
    }).encode()
    # HTTP basic auth
    import base64
    auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 201)
    except Exception:
        return False

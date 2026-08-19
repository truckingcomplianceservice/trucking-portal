# Trucking Compliance Services — Operations Portal

Auto-estimate loaded miles from stops (free, no API key).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: auto-estimate miles (Add Load page)
On the "+ New load" page, next to "Loaded miles" there's now an "auto-estimate"
link. Enter your stops as "City, ST" (e.g. Sacramento, CA), click auto-estimate,
and it fills in estimated loaded miles across all stops. You can always edit the
number by hand. Total miles (loaded + deadhead) still updates live.

HONEST NOTE: this is a FREE OFFLINE ESTIMATE (great-circle distance x a road
factor), typically within ~10-15% of actual road miles -- good for quick P&L,
but VERIFY for billing and IFTA. For exact road miles, we can add a Google Maps
API key later. Deadhead miles are still entered by hand (or estimate the leg
from your previous drop to this pickup).

Works with "City, ST" for major freight cities and all US states. If a stop
isn't recognized, it tells you which one to fix.

## Includes everything to date
Auto miles estimate, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, professional 1099, R2 cloud backup, multi-stop load, truck P&L date fix,
12-test suite, factoring, doc viewer, company docs, company logins, FMCSA lookup.

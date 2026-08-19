# Trucking Compliance Services — Operations Portal

Fix: vehicle Documents & Photos now show on the vehicle page (were hidden).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
On a vehicle's page, the Documents and Photos sections were not showing (a
template block was left open, so those sections were accidentally pushed into the
page title and never rendered). Now when you click a vehicle, you immediately see:
- Photos (add/view/delete)
- Documents (view / email / delete + upload form)
right on the page -- no need to click Edit.

## Includes everything to date
Vehicle page fix, deadhead fix + Google-ready miles, unified load form, vehicle
docs front, auto loaded miles, vehicle photos, email document, hiring phases 1-6,
dashboard KPIs, professional 1099, R2 cloud backup, multi-stop load, truck P&L
date fix, 12-test suite, factoring, doc viewer, company docs, company logins,
FMCSA lookup.

# Trucking Compliance Services — Operations Portal

Fix: ALL brokers show in the Brokers list (including ones with no loads yet).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
Before, the Brokers list only showed a broker if it already had at least one
load -- so a newly added broker (or one linked but not yet loaded) could be
missing from the list. Now EVERY broker appears in the Brokers list, with its
load count and revenue (shown as 0 until it has loads). Brokers you add from the
load form (or in Admin) now always show up in the list right away.

Load/revenue numbers are still scoped to your company (a company login sees its
own load counts), but the broker master list is shared.

## Includes everything to date
All-brokers list fix, brokers + agents, team messages, admin-only delete, vehicle
page fix, deadhead fix + Google-ready miles, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, professional 1099, R2 cloud backup, 12-test suite, factoring, company docs,
company logins, FMCSA lookup.

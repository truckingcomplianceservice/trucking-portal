# Trucking Compliance Services — Operations Portal

Fix: deadhead (empty) miles = ONLY the gap between the last load's drop and this
load's pickup (not measured from an earlier/first load).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
The deadhead "auto" button was, in some cases, picking the wrong previous load
(e.g. an old first load) because loads without delivery dates confused the
ordering. Now it reliably takes the driver/truck's MOST RECENTLY COMPLETED load
(the one with the latest delivery date) and measures empty miles ONLY from that
drop-off to the new load's pickup -- the normal, correct deadhead.

Example: last load delivered in Phoenix, new load picks up in Las Vegas ->
deadhead = Phoenix to Las Vegas (~307 mi). It will NOT measure from New York or
any earlier load.

Still: uses exact Google miles if GOOGLE_MAPS_API_KEY is set, else free estimate;
you can always edit the number by hand.

## Includes everything to date
Deadhead fix + Google-ready miles, unified load form, vehicle docs front, auto
loaded miles, vehicle photos, email document, hiring phases 1-6, dashboard KPIs,
professional 1099, R2 cloud backup, multi-stop load, truck P&L date fix,
12-test suite, factoring, doc viewer, company docs, company logins, FMCSA lookup.

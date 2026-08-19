# Trucking Compliance Services — Operations Portal

Ab har jagah SAME complete load form (stops/miles + documents + payment status).

## Deploy
1. Zip download karein, phir Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop → Commit → Push. Incognito me test karein.

## Kya theek hua (What changed)
Pehle load 2 jagah se add hota tha aur farq tha:
- Dispatch ka "+ New load" = achha form (stops/miles) but no documents / no payment status
- Dashboard ka "+ New load" = purana Admin form (basic)

Ab DONO jagah ka button SAME achhe form par jata hai, aur us form me ab ye sab hai:
- Multiple stops / segments (LTL) + add/remove
- Loaded + deadhead miles with auto-estimate + live total
- Rate, dates, driver, truck
- NEW: Load status (Booked/Dispatched/In transit/Delivered/Invoiced/Paid)
- NEW: Payment status (Unpaid/Submitted to factor/Advanced/Reserve released/Closed)
- NEW: Documents upload right on the form — Rate confirmation, BOL, POD
  (aur baad me load ki page se aur bhi documents add kar sakte hain)

Dashboard ke dono "+ New load" links ab is form par jaate hain (Admin par nahi).

## Includes everything to date
Unified load form, vehicle docs front, auto miles, vehicle photos, email document,
hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup, multi-stop
load, truck P&L date fix, 12-test suite, factoring, doc viewer, company docs,
company logins, FMCSA lookup.

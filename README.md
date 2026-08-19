# Trucking Compliance Services — Operations Portal (COMPLETE)

Dashboard KPIs: profit/loss + top drivers, trucks, and team at a glance.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: dashboard KPIs (top of Dashboard)
- Profit & Loss (this year): Revenue (YTD + this month), Costs (fuel+pay+maint+
  expenses), Profit, Loads count.
- More KPIs: Driver pay YTD, Fuel YTD, Active trucks, Team members.
- Top drivers table: loads, revenue, miles, paid -- each links to their report.
- Top trucks table: loads, revenue, miles, net -- each links to its P&L.
Everything respects the company switcher (one company or all).

## Includes everything to date
Dashboard KPIs, professional 1099, R2 cloud backup, multi-stop load, truck P&L
date fix, test suite, factoring, doc viewer, company docs, company logins, FMCSA.

# Trucking Compliance Services — Operations Portal

Driver wages now also show on the single-truck report (the page you land on when
you click a truck), not just the per-truck P&L table.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
There are two truck reports:
1. Reports -> "Per-truck P&L" = a TABLE of all trucks (already had Driver wages).
2. Clicking a truck row (or a truck on the dashboard) opens the SINGLE-TRUCK
   report for that unit -- THIS page was missing driver wages. That's the page you
   were looking at for Unit 1604.

Now the single-truck report shows a "Driver wages" box and subtracts wages from
the truck's Net -- matching the per-truck P&L table and the vehicle page. The PDF
download for a truck includes wages too.

WAGES STILL REQUIRE THE DATA CHAIN: a paid driver settlement, whose driver's
loads carry that truck, with pickup dates inside the settlement's pay period. If a
truck shows $0 wages, its loads are probably missing the truck or driver, or the
dates don't line up.

## Includes everything to date
Wages on single-truck report, reports label fix, per-truck driver-wage
attribution, team invite + approval, per-truck P&L expense fix, improved rate-con
broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet,
company switcher fix, deadhead nearby-city fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

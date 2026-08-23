# Trucking Compliance Services — Operations Portal

Per-truck P&L now includes driver wages, attributed to each truck.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
When you paid driver wages (a settlement), it was NOT being counted against any
specific truck in the per-truck P&L. So a truck's net looked too high.

Now the per-truck P&L has a "Driver wages" column, and net =
   revenue - fuel - maintenance - expenses - driver wages

HOW WAGES ARE ATTRIBUTED TO A TRUCK (since a driver can drive any truck):
- For each driver settlement, the app looks at the loads that driver ran during
  that pay period and which truck each load was on.
- The wages are split across those trucks BY LOAD REVENUE. Example: a driver paid
  $1,000 who ran $6,000 of loads on Truck A and $2,000 on Truck B gets $750
  charged to A and $250 to B.
- If the driver ran loads on only one truck that period, all their wages go to
  that truck.
- If a settlement has no matching truck-loads in its period, those wages can't be
  tied to a truck and are left out of the per-truck view (they're still in the
  driver's settlement and company P&L).

IMPORTANT: for wages to land on the right truck, your loads must have BOTH the
driver AND the truck set, and the load's pickup date must fall in the driver's
settlement period. The more complete your load data, the more accurate this is.

## Includes everything to date
Per-truck driver-wage attribution, team invite + approval, per-truck P&L expense
fix, improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense
fix, IFTA worksheet, company switcher fix, deadhead nearby-city fix + auto-fill,
chat + task files, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

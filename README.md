# Trucking Compliance Services — Operations Portal

Fix: per-truck P&L now includes expenses added in Accounting.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
The per-truck Profit & Loss statement was calculating net as:
   revenue - fuel - maintenance
It completely LEFT OUT expenses you add in Accounting (tires, insurance, wages,
tolls, etc.) tied to that truck. So a truck's net profit looked higher than it
really was.

Now the per-truck P&L has an "Expenses" column and calculates:
   net = revenue - fuel - maintenance - expenses
Both the on-screen report and the PDF are fixed. Example: revenue $5,000, fuel
$1,000, maintenance $500, expenses $300 -> net $3,200 (was wrongly $3,500).

This matches the earlier fixes that added expenses to the vehicle page and the
cost breakdown -- now the per-truck P&L agrees with them.

NOTE: for an expense to count for a truck, it must be tied to that truck (pick the
truck when adding the expense in Accounting). Company-wide expenses with no truck
selected won't appear in a single truck's P&L (they're in the company P&L).

## Includes everything to date
Per-truck P&L expense fix, improved rate-con broker auto-add, vehicle cost %
breakdown, vehicle-expense display fix, IFTA worksheet, company switcher fix,
deadhead nearby-city fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

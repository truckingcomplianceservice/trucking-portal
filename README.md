# Trucking Compliance Services — Operations Portal

Driver wages now have a full detail breakdown on the single-truck report.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Driver wages detail
Before, the single-truck report showed only the TOTAL driver wages. Now, like
fuel/maintenance/expenses, there's a "Driver wages detail" table showing every
settlement that makes up that total:
- Driver name
- Pay period (dates)
- Paid / unpaid status (and paid date)
- How many loads on THIS truck in that period
- The full settlement amount
- The portion charged to THIS truck (with a "split N trucks" note if the driver
  ran more than one truck that period)
- A grand total at the bottom

So you can now see exactly which pay periods and drivers make up a truck's wage
cost, not just the lump sum.

## Includes everything to date
Driver wages detail, wages on single-truck report, reports label fix, per-truck
driver-wage attribution, team invite + approval, per-truck P&L expense fix,
improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead nearby-city fix + auto-fill, chat +
task files, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

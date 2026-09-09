# Trucking Compliance Services — Operations Portal

Check stub now lists the loads covered (date, load #, route, rate).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new on the printed check stub
The pay stub (bottom of the LMP100 check) now shows, above the money breakdown, a
"Loads paid" table:
  Date   Load #     Route                    Rate
  08/24  TQL-8842   Dallas TX -> Miami FL     $1,800.00
  08/27  RXO-1120   Miami FL -> Atlanta GA      $700.00
  Loads total                                 $2,500.00
...followed by the existing gross / deductions / reimbursements (with itemized
lines) / net pay. So the driver's check stub now shows BOTH which loads it covers
AND the full pay math.

Note: if a settlement has many loads, the list can get long for the stub space.
For typical weekly settlements (a handful of loads) it fits well. If you ever pay
a settlement with a very large number of loads and it crowds the stub, tell me and
I'll switch to a compact one-line-per-load format.

## Includes everything to date
Loads on check stub, LMP100 check layout + itemized lines, load photos gallery,
driver check printing, invoice load search, invoice auto-fill from load, P&L miles
+ $/mi, auto loaded-miles, invoice unpaid-until-recorded, invoice custom line items
+ email, searchable load picker, settlement wage calculator,
daily/per-load/percentage settlements, driver-only load picker, settlement PDF
itemized fix, itemized settlement lines, driver settlement detail, settlement
layout fix, easy driver-wage creation, rental truck swap, photo viewer signed-URL
fix, truck photo gallery, office PWA + mobile layout, phone tap-to-call/text +
phone login + SMS-ready, driver nav + stop status + scanner, dismissible location
notice, driver map coordinates, driver location tracking + live map, driver PWA
app, driver load detail, driver login fix, driver invite links,
create-driver-login button, driver portal, IFTA print, broker detail page, driver
wages detail, wages on single-truck report, per-truck driver-wage attribution,
team invite + approval, per-truck P&L expense fix, improved rate-con broker
auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet, company
switcher fix, deadhead fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

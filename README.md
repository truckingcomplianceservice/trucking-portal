# Trucking Compliance Services — Operations Portal

Drivers can now see the FULL breakdown of each settlement in their app.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: driver settlement detail (in the driver app)
Before, a driver saw only a list with net pay. Now they can TAP any settlement in
"My Pay" and see the full detail:

- PAY BREAKDOWN: gross pay, deductions, reimbursements (out-of-pocket), extra
  reimbursement, and the final net pay -- so they see exactly how it adds up.
- LOADS IN THIS PAY: every load the settlement covers (date, route, ref, and rate
  if you allow drivers to see rates), with a loads total.
- REIMBURSED EXPENSES: the out-of-pocket expenses they submitted in that period
  (tolls, etc.) that were added to their pay -- date, what, amount.
- If paid: shows the method and reference (e.g. "Paid by Zelle - ref Z123").
- Any notes you added to the settlement.

RATE PRIVACY respected: load rates only show if your "Drivers can see load rate"
setting is on AND the settlement isn't set to hide amounts.
SECURITY: a driver can only open their OWN settlements.

## Includes everything to date
Driver settlement detail, settlement layout fix, easy driver-wage creation, rental
truck swap, photo viewer signed-URL fix, truck photo gallery, office PWA + mobile
layout, phone tap-to-call/text + phone login + SMS-ready, driver nav + stop status
+ scanner, dismissible location notice, driver map coordinates, driver location
tracking + live map, driver PWA app, driver load detail, driver login fix, driver
invite links, create-driver-login button, driver portal, IFTA print, broker detail
page, driver wages detail, wages on single-truck report, per-truck driver-wage
attribution, team invite + approval, per-truck P&L expense fix, improved rate-con
broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet,
company switcher fix, deadhead fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

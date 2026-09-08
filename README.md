# Trucking Compliance Services — Operations Portal

Fix: newest loads now appear in the invoice "Link a load" list (+ searchable).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What was wrong
The invoice "Link a load" dropdown pulled loads in no particular order and capped
the list, so once you had a lot of loads, a NEW load (like your truck-786 one)
often wasn't in the shown batch -- making it look missing.

## The fix
- The list is now ordered NEWEST FIRST and covers many more loads, so recent loads
  always show up.
- It's now a SEARCH box + list: type a load number, a truck number (e.g. 786), or a
  city to filter instantly.
- Each option shows: reference - Truck # - origin->destination - $rate - date.
- Picking a load still auto-fills the subtotal and broker.

So to invoice the truck-786 load: Billing -> New invoice -> type "786" (or the load
number) in the load search -> pick it -> subtotal auto-fills -> Create invoice.

## Includes everything to date
Invoice load list newest-first + searchable, invoice auto-fill from load, P&L
miles + $/mi, auto loaded-miles, invoice unpaid-until-recorded, invoice custom line
items + email, searchable load picker, settlement wage calculator,
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

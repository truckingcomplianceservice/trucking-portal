# Trucking Compliance Services — Operations Portal

Expense form now has a "Paid by" dropdown: Company / Partner / Driver.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: "Paid by" on every expense
When you add an expense (Accounting -> add expense), there's now a "Paid by"
dropdown:
- Company (business account/card) -- the default, a normal company expense.
- Partner: [name] (out of pocket) -- records it as that partner's contribution in
  the Partner ledger. Set a Truck too and it shows under that truck.
- Driver: [name] (out of pocket) -- flags it as a driver reimbursement (feeds
  their settlement's out-of-pocket reimbursements).

One dropdown answers "whose money paid this?" and routes it to the right place
automatically -- no separate checkboxes to remember.

## Includes everything to date
Expense "Paid by" dropdown, partner ledger + 500 fix, loads on check stub, LMP100
check layout, load photos gallery, driver check printing, invoice load search,
invoice auto-fill from load, P&L miles + $/mi, auto loaded-miles, invoice
unpaid-until-recorded, invoice custom line items + email, searchable load picker,
settlement wage calculator, daily/per-load/percentage settlements, driver-only
load picker, settlement PDF itemized fix, itemized settlement lines, driver
settlement detail, settlement layout fix, easy driver-wage creation, rental truck
swap, photo viewer signed-URL fix, truck photo gallery, office PWA + mobile
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

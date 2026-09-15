# Trucking Compliance Services — Operations Portal

Pay a driver's check to their COMPANY name (owner-operator business name).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: "Pay checks to" business name per driver
Many drivers are owner-operators paid as a company (e.g. "Singh Trucking LLC")
instead of their personal name. Now you can set that:

1. Go to Drivers -> click the driver.
2. In the new "Pay checks to" card, type the business name (e.g. Singh Trucking
   LLC) and Save. Leave it blank to pay the driver's personal name.
3. When you print that driver's check, the payee line shows the BUSINESS NAME.
   Drivers without a business name still print with their personal name.

This only changes the payee (who the check is made out to). The pay stub still
shows the driver's settlement details as before.

## Includes everything to date
Driver "pay checks to" business name, IFTA CSV import, P&L partner breakdown,
partner statement, expense "Paid by" dropdown, partner ledger, loads on check
stub, LMP100 check layout, load photos gallery, driver check printing, invoice
load search, invoice auto-fill from load, P&L miles + $/mi, auto loaded-miles,
invoice unpaid-until-recorded, invoice custom line items + email, searchable load
picker, settlement wage calculator, daily/per-load/percentage settlements,
driver-only load picker, settlement PDF itemized fix, itemized settlement lines,
driver settlement detail, settlement layout fix, easy driver-wage creation, rental
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

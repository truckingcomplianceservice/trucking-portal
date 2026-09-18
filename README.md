# CarrierConnect360 — multi-stop with date/time/appointment per stop

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## New: each stop has its own date, time & appointment number
The add-load form's Stops section is upgraded. Each stop is now its own card with:
- Location (city/state or full address)
- Date
- Time / time window (e.g. "8am-12pm")
- Appointment / PO number
"+ Add another stop" adds more; first = Pickup, last = Delivery, middle = Stop.

The load detail page shows a clean Stops table: #, type, location, date, time,
and appointment/PO -- so dispatchers and drivers see each stop's appointment.
(Old text-only stops on existing loads still display; new loads use the
structured stops.)

## Also (already in AUG22y): co-driver on the add-load form + team 50/50 pay.

## Includes everything to date
Structured multi-stop (date/time/appt), team driver support, onboarding checklist +
password reset, white-label company logo on reports, rate con full-address fix,
IFTA ELD reconciliation, automatic IFTA + per-truck, logo squish fix, adaptive
logo, light landing page, multi-domain, staff-entered application, email
verification, terminate/rehire, driver counts + complete-record-on-hire, verified
e-consent, FMCSA road test, FMCSA application form, driver email login, DQF EPN +
email app link + expiration reminders, FMCSA DQF, settlement search, check amount
nudge, self-serve signup + trial, hide-load-amounts, owner-operator EIN/1099,
driver pay-to business name, IFTA CSV import, P&L partner breakdown, partner
statement, expense Paid-by, partner ledger, loads on check stub, LMP100 check
layout, load photos, driver check printing, invoice load search + auto-fill, P&L
miles + $/mi, auto loaded-miles, invoice unpaid-until-paid, invoice line items +
email, searchable load picker, wage calculator, settlements basis options,
driver-only load picker, settlement PDF itemized, itemized lines, driver settlement
detail, settlement layout fix, easy wage creation, rental truck swap, photo viewer
fix, truck photo gallery, office PWA + mobile, phone tap-to-call + phone login +
SMS-ready, driver nav + status + scanner, location notice, driver map, driver
tracking, driver PWA, driver load detail, driver login fix, driver invite links,
create-driver-login, driver portal, IFTA print, broker detail, driver wages
detail, per-truck wages, team invite, per-truck P&L fix, rate-con auto-add,
vehicle cost %, vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead
fix, chat + task files, notifications, chat mentions, team tools, rate-con
protection, brokers + agents, admin delete, vehicle fix, unified load form, auto
miles, vehicle photos, email doc, hiring 1-6, dashboard KPIs, 1099, R2 backup,
tests, factoring, company docs, company logins, FMCSA lookup.

# CarrierConnect360 — team driver support

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## New: team driver (two drivers on one truck/load)
- The load form now has a "Co-driver (team)" dropdown next to Driver. Pick a
  second driver for team-driven loads.
- BOTH the driver and the co-driver see the load in their own driver app (loads,
  status, navigate, documents).
- On the settlement, a new "Team split 50/50" button sets this driver's gross to
  half the loads' total -- do the same on the co-driver's settlement and each gets
  their 50%.
So a team-driven truck is fully supported: assign both drivers, both see the work,
and pay splits 50/50.

## HOW TO USE for a team truck
1. Create/edit the load -> set Driver = first driver, Co-driver = second driver.
2. Both drivers see it in their app.
3. Create a settlement for driver 1 -> add the team loads -> click "Team split
   50/50" (driver 1 gets half). Create a settlement for driver 2 -> same loads ->
   "Team split 50/50" (driver 2 gets the other half).

## Includes everything to date
Team driver support, onboarding checklist + password reset, white-label company
logo on reports, rate con full-address fix, IFTA ELD reconciliation, automatic
IFTA + per-truck, logo squish fix, adaptive logo, light landing page, multi-domain,
staff-entered application, email verification, terminate/rehire, driver counts +
complete-record-on-hire, verified e-consent, FMCSA road test, FMCSA application
form, driver email login, DQF EPN + email app link + expiration reminders, FMCSA
DQF, settlement search, check amount nudge, self-serve signup + trial,
hide-load-amounts, owner-operator EIN/1099, driver pay-to business name, IFTA CSV
import, P&L partner breakdown, partner statement, expense Paid-by, partner ledger,
loads on check stub, LMP100 check layout, load photos, driver check printing,
invoice load search + auto-fill, P&L miles + $/mi, auto loaded-miles, invoice
unpaid-until-paid, invoice line items + email, searchable load picker, wage
calculator, settlements basis options, driver-only load picker, settlement PDF
itemized, itemized lines, driver settlement detail, settlement layout fix, easy
wage creation, rental truck swap, photo viewer fix, truck photo gallery, office PWA
+ mobile, phone tap-to-call + phone login + SMS-ready, driver nav + status +
scanner, location notice, driver map, driver tracking, driver PWA, driver load
detail, driver login fix, driver invite links, create-driver-login, driver portal,
IFTA print, broker detail, driver wages detail, per-truck wages, team invite,
per-truck P&L fix, rate-con auto-add, vehicle cost %, vehicle-expense fix, IFTA
worksheet, company switcher fix, deadhead fix, chat + task files, notifications,
chat mentions, team tools, rate-con protection, brokers + agents, admin delete,
vehicle fix, unified load form, auto miles, vehicle photos, email doc, hiring 1-6,
dashboard KPIs, 1099, R2 backup, tests, factoring, company docs, company logins,
FMCSA lookup.

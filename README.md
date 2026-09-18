# Trucking Compliance Services — Operations Portal

Team members can fill out a driver application on the driver's behalf.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: staff-entered driver application
On the Hiring page there's a new "+ Add application" button. A logged-in team
member (admin, manager, dispatcher, safety, or compliance) can fill out the full
FMCSA application FOR a driver who can't do it themselves.
- Same fields as the driver's own application (personal, license, history,
  driving record, documents, certification).
- No email verification needed (staff is entering it, not the driver).
- It records WHO entered it and when, in the application notes (audit trail).
- Creates the same application record -- you can then convert to a driver and build
  their DQF, exactly like a driver-submitted application.

So you now have both paths: the driver fills it out via their emailed link, OR your
team fills it out for them.

## Includes everything to date
Staff-entered application, email verification (signup + application),
terminate/rehire (FMCSA reset), driver active/inactive counts +
complete-record-on-hire, verified driver e-consent, FMCSA road test, FMCSA
application form, driver email login, DQF EPN + email app link + expiration
reminders, FMCSA DQF (Part 391), settlement search, check amount nudge, rebrand,
self-serve signup + trial, hide-load-amounts, owner-operator EIN/1099, driver
pay-to business name, IFTA CSV import, P&L partner breakdown, partner statement,
expense Paid-by, partner ledger, loads on check stub, LMP100 check layout, load
photos, driver check printing, invoice load search + auto-fill, P&L miles + $/mi,
auto loaded-miles, invoice unpaid-until-paid, invoice line items + email,
searchable load picker, wage calculator, settlements basis options, driver-only
load picker, settlement PDF itemized, itemized lines, driver settlement detail,
settlement layout fix, easy wage creation, rental truck swap, photo viewer fix,
truck photo gallery, office PWA + mobile, phone tap-to-call + phone login +
SMS-ready, driver nav + status + scanner, location notice, driver map, driver
tracking, driver PWA, driver load detail, driver login fix, driver invite links,
create-driver-login, driver portal, IFTA print, broker detail, driver wages
detail, per-truck wages, team invite, per-truck P&L fix, rate-con auto-add,
vehicle cost %, vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead
fix, chat + task files, notifications, chat mentions, team tools, rate-con
protection, brokers + agents, admin delete, vehicle fix, unified load form, auto
miles, vehicle photos, email doc, hiring 1-6, dashboard KPIs, 1099, R2 backup,
tests, factoring, company docs, company logins, FMCSA lookup.

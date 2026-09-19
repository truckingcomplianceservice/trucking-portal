# CarrierConnect360 — live chat on the public homepage too

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Hard refresh in incognito.

## What changed
Tawk.to live chat now also appears on the PUBLIC homepage
(www.carrierconnect360.com), not just inside the app. So:
- Website VISITORS (not logged in) can live-chat with you before signing up --
  great for answering "how much?", "do you support X?" and converting them.
- Logged-in CLIENTS get the full support (smart AI with their data + live chat +
  email), as before.
Uses the same TAWK_ID Railway variable you already set -- no new setup.

Summary of where support shows now:
- Public homepage: Tawk.to live chat.
- Inside the app: smart AI (app + website + client's own data) + live chat + email.

## Includes everything to date
Live chat on homepage, smart AI support (own data, scoped) + live agent + email,
logo sizing fix, structured multi-stop, team driver, onboarding + password reset,
white-label logo on reports, rate con full-address fix, IFTA ELD reconciliation,
automatic IFTA + per-truck, adaptive logo, light landing page, multi-domain,
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

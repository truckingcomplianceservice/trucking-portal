# CarrierConnect360 — rate con captures FULL address

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## What was wrong + fixed
Rate con upload was only capturing partial addresses. Two fixes:
1. The origin/destination fields were capped at 120 characters -- long full
   addresses got cut off. Expanded to 255.
2. The AI extraction prompt now explicitly asks for the FULL pickup and delivery
   address (street, city, state, ZIP), not just city/state.

## LIKELY ROOT CAUSE -- please check this
If it "was working yesterday" and suddenly only grabs city/state, the most likely
cause is your ANTHROPIC_API_KEY (used for the smart extraction) stopped working --
expired, out of credits, or rate-limited. When the AI key fails, the system falls
back to a simple text scan that only finds "City, ST" -- NOT the full street
address. That matches your symptom exactly.

TO CHECK: in Railway -> Variables, confirm ANTHROPIC_API_KEY is still set and valid,
and check your Anthropic account has credit / isn't rate-limited. On the rate-con
upload page, it says whether AI extraction is ON. If AI is off, extraction is
city-only by design. Re-add a working key to restore full-address extraction.

## Includes everything to date
Rate con full-address fix, IFTA ELD reconciliation, automatic IFTA + per-truck,
logo squish fix, adaptive logo, light landing page, multi-domain, staff-entered
application, email verification, terminate/rehire, driver counts +
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

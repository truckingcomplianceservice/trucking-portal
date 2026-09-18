# Trucking Compliance Services — Operations Portal

FMCSA-compliant driver APPLICATION FORM (§391.21) + the DQF checklist.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new: the driver application form now meets FMCSA §391.21
The application a driver fills out (via the emailed link or /apply/<token>/) now
collects everything §391.21 requires, organized into sections:

PERSONAL: name, date of birth, phone, email, emergency contact, current address,
  3-year address history.
LICENSE (§391.21): CDL number, class, state, expiration, hazmat/TWIC, and all
  OTHER licenses held in the past 3 years.
LICENSE HISTORY: ever denied a license? ever suspended/revoked? + explanation.
EMPLOYMENT HISTORY (last 10 years): with the existing 10-year employment text.
DRIVING RECORD: traffic convictions in the past 12 months (or None), accidents in
  the past 3 years (or None).
DOCUMENTS: CDL, medical certificate, other.
CERTIFICATION & CONSENT: authorizes MVR/PSP/drug-alcohol/Clearinghouse checks; the
  typed signature is captured with an audit record (IP, device, timestamp, hash).

So both parts are now FMCSA-aligned: the APPLICATION (what the driver fills in) and
the DQF FILE checklist (what you track/keep on file, 49 CFR Part 391).

## Where to see each
- Application form: Drivers page has the apply link, or email it from the DQF page,
  or /apply/<company token>/. This is what the DRIVER fills out.
- DQF checklist: Drivers -> a driver -> "DQF file". This is what YOU track.

IMPORTANT: this follows FMCSA requirements but is not legal advice -- have a DOT
compliance professional confirm it matches current rules before relying on it or
selling it as compliant.

## Includes everything to date
FMCSA application form (§391.21), driver email login, DQF EPN + email app link +
expiration reminders, FMCSA DQF (Part 391), settlement search, check amount nudge,
rebrand, self-serve signup + trial, hide-load-amounts, owner-operator EIN/1099,
driver pay-to business name, IFTA CSV import, P&L partner breakdown, partner
statement, expense Paid-by, partner ledger, loads on check stub, LMP100 check
layout, load photos, driver check printing, invoice load search + auto-fill, P&L
miles + $/mi, auto loaded-miles, invoice unpaid-until-paid, invoice line items +
email, searchable load picker, wage calculator, settlements basis options,
driver-only load picker, settlement PDF itemized, itemized lines, driver
settlement detail, settlement layout fix, easy wage creation, rental truck swap,
photo viewer fix, truck photo gallery, office PWA + mobile, phone tap-to-call +
phone login + SMS-ready, driver nav + status + scanner, location notice, driver
map, driver tracking, driver PWA, driver load detail, driver login fix, driver
invite links, create-driver-login, driver portal, IFTA print, broker detail,
driver wages detail, per-truck wages, team invite, per-truck P&L fix, rate-con
auto-add, vehicle cost %, vehicle-expense fix, IFTA worksheet, company switcher
fix, deadhead fix, chat + task files, notifications, chat mentions, team tools,
rate-con protection, brokers + agents, admin delete, vehicle fix, unified load
form, auto miles, vehicle photos, email doc, hiring 1-6, dashboard KPIs, 1099, R2
backup, tests, factoring, company docs, company logins, FMCSA lookup.

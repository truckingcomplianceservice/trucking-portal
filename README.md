# Trucking Compliance Services — Operations Portal

Verified driver e-consent (Clearinghouse etc.) — email code + last-4 SSN + signed PDF.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: verified driver consent + e-signature
On a driver's DQF file page, "Send a consent for the driver to e-sign". Choose:
- FMCSA Clearinghouse full-query consent (49 CFR 382.701)
- Clearinghouse limited-query (annual) consent
- MVR / PSP / background & drug-alcohol records consent (391.23 / 40.25)
- General application certification & consent
Enter the driver's email and send. The driver gets a secure link and:
1. Reads the consent text.
2. Requests a 6-DIGIT CODE (emailed to them) and enters it.
3. Enters the LAST 4 OF THEIR SSN (must match what you stored in Admin -> Driver
   -> "Last 4 of SSN"). Only last-4 is stored, never the full SSN.
4. Types their name and signs.
The system records: signed timestamp, email-verified, SSN-matched, IP, device, and
a tamper-evident SHA-256 hash. A signed CONSENT PDF (with the full audit record) is
available for the file, and the matching DQF item is marked complete.

SETUP: put each driver's last-4 SSN in Admin -> Drivers -> "Last 4 of SSN" so the
identity match works. (If left blank, the code-only verification still works.)

## HONEST / LEGAL notes
- This is a strong, verified e-signature with an audit trail, but it is NOT legal
  advice. Have a compliance attorney confirm it meets ESIGN/UETA and FMCSA needs
  before relying on it or selling it as compliant.
- FMCSA Clearinghouse FULL queries also require the driver's consent INSIDE the
  Clearinghouse system (login.gov) -- this form documents your consent step but does
  not replace the Clearinghouse's own consent. The consent text says so.
- We store only the LAST 4 of SSN, by design, to reduce risk. Do not store full SSNs.

## Includes everything to date
Verified driver e-consent, FMCSA road test, FMCSA application form, driver email
login, DQF EPN + email app link + expiration reminders, FMCSA DQF (Part 391),
settlement search, check amount nudge, rebrand, self-serve signup + trial,
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

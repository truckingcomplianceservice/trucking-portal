# Trucking Compliance Services — Operations Portal

Check amount: moved up to the $ sign line + live nudge buttons to fine-tune it.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## The fix (amount was printing too low)
- The dollar amount now defaults higher, on the same line as the $ sign.
- NEW: on the check page there are live nudge buttons -- Up, Down, Left, Right,
  Reset -- to move the amount. Each click moves it a little and saves automatically.
  So you can line it up perfectly on your exact checks without editing Admin:
    1. Open a settlement -> Print check.
    2. Print on plain paper, hold against a real check.
    3. If the amount is a bit low, click "Up" once or twice; too high, click "Down";
       sideways, use Left/Right.
    4. Re-print and check. Repeat until it sits right next to the $ sign.
  Once set, it stays for all future checks. "Reset" puts it back to default.

## Includes everything to date
Check amount nudge + alignment, rebrand to Trucking Compliance Services,
self-serve signup + 7-day trial + subscription page, hide-load-amounts
consistency, owner-operator company pay + EIN on 1099, driver pay-to business
name, IFTA CSV import, P&L partner breakdown, partner statement, expense Paid-by,
partner ledger, loads on check stub, LMP100 check layout, load photos, driver
check printing, invoice load search + auto-fill, P&L miles + $/mi, auto
loaded-miles, invoice unpaid-until-paid, invoice line items + email, searchable
load picker, wage calculator, daily/per-load/percentage settlements, driver-only
load picker, settlement PDF itemized, itemized settlement lines, driver settlement
detail, settlement layout fix, easy driver-wage creation, rental truck swap, photo
viewer fix, truck photo gallery, office PWA + mobile, phone tap-to-call + phone
login + SMS-ready, driver nav + status + scanner, location notice, driver map,
driver tracking, driver PWA, driver load detail, driver login fix, driver invite
links, create-driver-login, driver portal, IFTA print, broker detail, driver wages
detail, per-truck wages, team invite, per-truck P&L fix, rate-con auto-add,
vehicle cost %, vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead
fix, chat + task files, notifications, chat mentions, team tools, rate-con
protection, brokers + agents, admin delete, vehicle fix, unified load form, auto
miles, vehicle photos, email doc, hiring 1-6, dashboard KPIs, 1099, R2 backup,
tests, factoring, company docs, company logins, FMCSA lookup.

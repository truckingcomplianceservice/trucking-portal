# CarrierConnect360 — logo adapts to each space

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Hard refresh (Cmd+Shift+R) in incognito.

## What changed: the logo now fits wherever it's shown
- Website header (wide): full shield + CarrierConnect360 wordmark, scaled to the
  header. On a narrow PHONE, it automatically switches to just the shield icon
  (a wide wordmark would be too tiny on a phone).
- App sidebar (wide): the wordmark, scaled to the sidebar width. When the sidebar
  COLLAPSES to a narrow strip (small screens), it automatically switches to just
  the shield icon so it still shows clearly.
- Tab / phone app icon: the shield only.
So the logo always shows at the right size for the space it's in -- full logo where
there's room, shield-only where it's tight.

## Includes everything to date
Adaptive logo, full logo on left, logo everywhere, light landing page,
multi-domain, staff-entered application, email verification, terminate/rehire,
driver counts + complete-record-on-hire, verified e-consent, FMCSA road test,
FMCSA application form, driver email login, DQF EPN + email app link + expiration
reminders, FMCSA DQF, settlement search, check amount nudge, self-serve signup +
trial, hide-load-amounts, owner-operator EIN/1099, driver pay-to business name,
IFTA CSV import, P&L partner breakdown, partner statement, expense Paid-by, partner
ledger, loads on check stub, LMP100 check layout, load photos, driver check
printing, invoice load search + auto-fill, P&L miles + $/mi, auto loaded-miles,
invoice unpaid-until-paid, invoice line items + email, searchable load picker, wage
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

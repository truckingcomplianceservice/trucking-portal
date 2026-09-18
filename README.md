# CarrierConnect360 — Operations Portal + Landing Page

Real, working marketing landing page at your domain root.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new: the selling landing page
Visiting your domain root (e.g. https://www.carrierconnect360.com) now shows a
professional marketing page (matches your CarrierConnect360 design: navy + gold):
- Sticky nav with logo, Features / How it works / Pricing, Log in, Start free trial.
- Hero: "One platform to run your whole fleet" + Start 7-day free trial button +
  stats strip (1 place / 7 days free / $100/mo).
- Features: 6 cards (dispatch, driver app, pay & checks, invoicing, FMCSA
  compliance, accounting & IFTA).
- How it works: a video placeholder (click the play button -- you add your tutorial
  video later) + a 4-step "up and running in minutes".
- Pricing: $100/mo (1-5 trucks) + $20/truck, with the included list + trial button.
- Final call-to-action + footer ("a Trucking Compliance Services product").

HOW IT WORKS:
- Logged-OUT visitors see this landing page at "/".
- All the "Start free trial" buttons go to /signup/ (7-day trial).
- "Log in" goes to /login/ (into the app).
- Logged-IN users visiting "/" are sent straight to their dashboard (so your
  existing users aren't shown the marketing page).

## To add your tutorial video later
Record a walkthrough (you have the video script), upload it (YouTube/Vimeo or a
file), and tell me -- I'll embed it in the "See it in action" section replacing the
placeholder play button.

## NOTE
The app itself still says "Trucking Compliance Services" inside (dashboard, etc.).
Next step (say the word): rebrand the whole app UI to CarrierConnect360 to match.

## Includes everything to date
Landing page, multi-domain ALLOWED_HOST, staff-entered application, email
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

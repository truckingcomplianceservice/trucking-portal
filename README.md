# CarrierConnect360 — live agent chat (Tawk.to) + AI support

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## Set up Tawk.to (free live chat) -- 5 minutes:
1. Go to tawk.to and create a free account.
2. It gives you a "Property ID" and "Widget ID" -- your embed URL looks like:
   https://embed.tawk.to/XXXXXXXXXXXX/YYYYY
   Copy the part after embed.tawk.to/  -> "XXXXXXXXXXXX/YYYYY"
3. In Railway -> Variables, add:  TAWK_ID = XXXXXXXXXXXX/YYYYY
4. Save (Railway redeploys). Done -- live chat is now on your app.
5. Install the Tawk.to mobile app so you can answer clients from your phone.

## How support now works (AI + live agent)
The "💬 Help" button opens the support panel with:
- AI assistant (instant answers) -- as before.
- "Talk to a human (email)" -- creates a ticket + emails your team.
- "Live chat with an agent" -- opens Tawk.to real-time chat with you/your agents.
  (This button only appears when TAWK_ID is set.)
So: AI handles most questions instantly; live chat connects clients to a real
person in real time; email ticket is the fallback when agents are offline.

If TAWK_ID is NOT set, the app works exactly as before (AI + email) with no live
chat button -- so it's safe to deploy now and add the ID whenever you're ready.

## Includes everything to date
Live agent (Tawk.to) + AI support, logo sizing fix, structured multi-stop, team
driver, onboarding + password reset, white-label logo on reports, rate con
full-address fix, IFTA ELD reconciliation, automatic IFTA + per-truck, adaptive
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

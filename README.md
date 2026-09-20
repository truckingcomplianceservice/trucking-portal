# CarrierConnect360 — dedicated Sales Dashboard for your sales team

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md static && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push.

## New: sales team gets their own workspace (same app, no extra cost)
You can now give a sales/marketing team member a login that lands them on the
SALES dashboard (leads pipeline), NOT the trucking TMS.

HOW TO SET UP A SALES PERSON:
1. Create their user (Admin -> Users -> add), or an existing staff user.
2. Admin -> Profiles -> their profile -> check "Sales/marketing team" -> save.
3. When they log in, they go straight to Sales / Leads and work leads/follow-ups.
   They see the sales system; they do NOT run the trucking side.

WHO SEES WHAT NOW:
- YOU (platform owner / superuser): everything -- TMS + Sales.
- SALES TEAM (is_sales_team on): the Sales dashboard (leads, follow-ups, ad
  tracking). Land there on login.
- CLIENTS (the carriers you sell to): only their TMS -- never the sales system.
- DRIVERS: only their driver app.

So it's like a separate sales portal in EXPERIENCE, but it's one app -- no second
deployment, no double maintenance, no extra Railway cost. When you hire sales, just
flip the "Sales team" checkbox on their profile.

## Includes everything to date
Dedicated sales dashboard for sales team, sales hidden from clients, Lead/CRM + ad
(UTM) tracking, homepage live chat, smart AI support, logo sizing fix, structured
multi-stop, team driver, onboarding + password reset, white-label logo on reports,
rate con full-address fix, IFTA ELD reconciliation, automatic IFTA + per-truck,
adaptive logo, light landing page, multi-domain, staff-entered application, email
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

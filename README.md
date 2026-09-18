# Trucking Compliance Services — Operations Portal

Drivers log in by EMAIL; one login covers loads, pay, AND documents.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new: one driver login for everything
- Drivers can now log in with their EMAIL (in addition to username or phone) at
  /login/. Whatever they type -- email, username, or phone -- it finds them.
- Once logged in, the SAME account gives the driver access to:
  * Their loads + load history + status/navigation
  * Upload BOL / POD
  * Add expenses
  * Their PAY / settlements + full pay-stub breakdown
  * NEW: "My documents & application" -- a link in the driver portal to fill out
    the application and upload their DQF documents (CDL, medical, etc.).
- So the driver you email the application link to can also just log in with their
  email and see loads + paystubs -- it's one connected experience.

HOW IT FITS TOGETHER:
- The emailed application link is a no-login page for quick onboarding uploads.
- Give the driver a login (Drivers -> Create driver login, or invite link) with
  their email, and that same email logs them into the full portal (loads, pay,
  documents). The login page now says "Username, email, or phone".

## Includes everything to date
Driver email login + unified portal access, DQF EPN + email app link + expiration
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

# Trucking Compliance Services — Operations Portal

DRIVER PORTAL: drivers log in and manage their own loads, uploads, expenses, pay.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Driver Portal (mobile-friendly)
Drivers now get their own simple, phone-friendly portal at /driver/. When a driver
logs in, they land there automatically (they never see your admin/office pages).

Each driver can:
- SEE THEIR LOADS: active loads on the home screen + full history under "My Loads".
- UPLOAD BOL / POD: on any of their loads, tap "Upload BOL / POD", pick photo or
  PDF. You (managers/dispatchers) get notified when a POD is uploaded.
- ADD EXPENSES: tap "+ Add an expense" -- category, amount, vendor, date, receipt
  photo, and an "I paid out of pocket (reimburse me)" checkbox. You get notified.
- SEE THEIR PAY: "My Pay" lists their settlements with paid/unpaid status and net
  pay, so they can see what they've been paid for.
- NOTIFICATIONS: a bell shows their unread count.

## Showing / hiding the load RATE to drivers
There's ONE global setting: Company -> "Drivers can see load rate ($)".
- OFF (default): drivers do NOT see any dollar rate on their loads.
- ON: drivers see the rate on their loads.
Set it in Admin -> Companies -> (your company) -> "Drivers can see load rate".

## Setting up a driver's login
In Admin -> Drivers -> (driver), set the "user" (login) field to a user account
for that driver. That links their login to their driver record. They then log in
with that username/password and land in the driver portal. (Next we can add
self-signup for drivers too, like the team invite links.)

## SECURITY (built in + tested)
- A driver sees ONLY their own loads, pay, and can only upload to their own loads.
- They cannot see other drivers' data, other trucks, or any office/admin pages.
- Tested: blocked from other drivers' loads, redirected to portal, non-drivers
  can't reach it.

## Includes everything to date
Driver portal, IFTA print, broker detail page, driver wages detail, wages on
single-truck report, per-truck driver-wage attribution, team invite + approval,
per-truck P&L expense fix, improved rate-con broker auto-add, vehicle cost %
breakdown, vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead
fix + auto-fill, chat + task files, notifications (bell+email) + task responses,
chat @mentions + chat-to-task, team username + remove, floating team chat +
handoff, duplicate rate-con protection, rate-con broker+agent auto-create,
all-brokers list, brokers + agents, admin-only delete, vehicle page fix, unified
load form, vehicle docs front, auto miles, vehicle photos, email document, hiring
phases 1-6, dashboard KPIs, 1099, R2 cloud backup, 12-test suite, factoring,
company docs, company logins, FMCSA lookup.

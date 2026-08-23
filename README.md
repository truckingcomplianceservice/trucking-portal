# Trucking Compliance Services — Operations Portal

Driver portal: tap a load to see miles + documents (BOL/POD/Rate con).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Driver load detail (in the driver portal)
Drivers can now TAP ANY LOAD (on Home or My Loads) to open its detail page, where
they see:
- MILES: loaded miles, empty (deadhead) miles, and total miles -- plus their truck.
- DOCUMENTS: Bill of Lading and Proof of Delivery, each with View + Download.
- RATE + RATE CONFIRMATION: shown ONLY if you've turned on
  Company -> "Drivers can see load rate ($)". If that's off, the driver sees no
  rate and no rate confirmation. If on, they see the rate and can View/Download
  the rate con.
- They can still upload BOL/POD right from the load.

SHARING: to send a document to someone, the driver taps Download, then uses their
phone's normal Share button to send it by text, email, or WhatsApp. (This is the
simplest, most reliable way on a phone -- no separate "send" system needed.)

SECURITY: a driver can only open THEIR OWN loads; trying to open another driver's
load is blocked. The rate con is gated behind the same rate-visibility setting.

## Includes everything to date
Driver load detail (miles + docs), driver login fix, driver invite links,
create-driver-login button, driver portal, IFTA print, broker detail page, driver
wages detail, wages on single-truck report, per-truck driver-wage attribution,
team invite + approval, per-truck P&L expense fix, improved rate-con broker
auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet, company
switcher fix, deadhead fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

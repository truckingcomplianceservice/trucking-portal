# Trucking Compliance Services — Operations Portal

Profit & Loss now shows loads, miles (loaded/empty/total), and $ per mile.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new on the Profit & Loss report
Each company row (and the totals row) now shows, alongside revenue:
- Loads (count)
- Loaded miles
- Empty (deadhead) miles
- TOTAL miles the trucks ran
- $/mi (revenue divided by total miles) -- a quick rate-per-mile figure

So you can see how many miles were run for the income earned, and your revenue per
mile, right on the P&L.

NOTE: miles come from what's entered on each load (loaded miles + deadhead miles).
The more complete your loads' mileage, the more accurate the totals. Loads with 0
miles simply don't add to the miles columns.

## Includes everything to date
P&L miles + $/mi, invoice unpaid-until-recorded, invoice custom line items +
email, searchable load picker, settlement wage calculator,
daily/per-load/percentage settlements, driver-only load picker, settlement PDF
itemized fix, itemized settlement lines, driver settlement detail, settlement
layout fix, easy driver-wage creation, rental truck swap, photo viewer signed-URL
fix, truck photo gallery, office PWA + mobile layout, phone tap-to-call/text +
phone login + SMS-ready, driver nav + stop status + scanner, dismissible location
notice, driver map coordinates, driver location tracking + live map, driver PWA
app, driver load detail, driver login fix, driver invite links,
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

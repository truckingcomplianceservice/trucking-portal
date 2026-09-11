# Trucking Compliance Services — Operations Portal

FIX: Partners page 500 error (active-company handling).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What was wrong
The Partners page tried to filter data by the "active company", but it was using
the raw session value (which can be the word "all" or a stale id) instead of a real
company record. On your live site your active company was "all", so the page
crashed with a 500. (It worked in testing only because the test happened to use a
real company id.)

## The fix
The Partners page (and the payback form) now properly resolve the active company to
a real company record, and fall back to your first company if it's set to "all" or
missing. No more crash.

Everything else about the partner ledger is unchanged and working:
contributions, paybacks, ownership %, profit share, per-truck breakdown.

## Includes everything to date
Partner ledger + 500 fix, loads on check stub, LMP100 check layout, load photos
gallery, driver check printing, invoice load search, invoice auto-fill from load,
P&L miles + $/mi, auto loaded-miles, invoice unpaid-until-recorded, invoice custom
line items + email, searchable load picker, settlement wage calculator,
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

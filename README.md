# Trucking Compliance Services — Operations Portal

Driver app: the "location is on" bar now shows once, then hides.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What changed
Before, the green "Location sharing is on" bar showed every time the driver opened
the app. Now it shows ONCE with a "Got it" link. When the driver taps "Got it",
the bar hides and stays hidden on that phone from then on.

IMPORTANT: location tracking itself is UNCHANGED -- it keeps working after the
driver dismisses the bar. The bar is only the notice; hiding it does NOT turn off
tracking. (The driver was informed once, which is the point.)

If the driver reinstalls the app or clears their browser data, the notice will
show once more -- which is fine and correct.

## Includes everything to date
Dismissible location notice, driver map coordinates + place + gmaps link, driver
location tracking + live map, driver PWA app, driver load detail, driver login
fix, driver invite links, create-driver-login button, driver portal, IFTA print,
broker detail page, driver wages detail, wages on single-truck report, per-truck
driver-wage attribution, team invite + approval, per-truck P&L expense fix,
improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

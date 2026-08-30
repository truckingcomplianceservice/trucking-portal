# Trucking Compliance Services — Operations Portal

Settlements: daily / per-load / percentage — all clear and easy.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## How to make each kind of settlement (Driver pay -> New driver wages)

DAILY:  Pay type -> "Daily (one day's loads)" -> pick the day. It attaches only
        that day's loads and pays for that day.

PER LOAD / ROUND TRIP:  Pay type -> "Per load / round trip" -> it starts empty and
        you click to add the exact loads you're paying for.

WEEKLY: Pay type -> "Weekly" -> pick the week; it attaches that week's loads.

PERCENTAGE (works with any of the above):
 - NEW: there's now a "Pay percentage (%)" box on the create form. Enter e.g. 25,
   and gross pay is set to 25% of the loads' total automatically.
 - Or set the driver's pay type to "Percentage of load" with a rate in
   Admin -> Drivers, and it auto-applies every time.
 - Or on the settlement page, use the "Apply %" box any time to recalculate.

So you can do: daily + percentage, per-load + percentage, weekly + percentage, or
flat dollar amounts -- whatever fits how you pay each driver.

## Includes everything to date
Daily/per-load/percentage settlements + % on create form, driver-only load picker,
settlement PDF itemized fix, itemized settlement lines, driver settlement detail,
settlement layout fix, easy driver-wage creation, rental truck swap, photo viewer
signed-URL fix, truck photo gallery, office PWA + mobile layout, phone
tap-to-call/text + phone login + SMS-ready, driver nav + stop status + scanner,
dismissible location notice, driver map coordinates, driver location tracking +
live map, driver PWA app, driver load detail, driver login fix, driver invite
links, create-driver-login button, driver portal, IFTA print, broker detail page,
driver wages detail, wages on single-truck report, per-truck driver-wage
attribution, team invite + approval, per-truck P&L expense fix, improved rate-con
broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet,
company switcher fix, deadhead fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

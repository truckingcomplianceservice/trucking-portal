# Trucking Compliance Services — Operations Portal

Settlement load picker shows ONLY that driver's loads.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What changed
When you open a driver's settlement, the "Add a load" picker now shows ONLY that
driver's own loads (that aren't already on a settlement). Other drivers' loads and
unassigned loads no longer appear -- so you can't add the wrong driver's load by
mistake. Remove also only affects this settlement's loads.

To pay a driver for a load that's currently under another driver, first change the
driver on that load (Loads -> the load -> Driver), then it appears in this picker.
Or use "Add a load manually" for a load not in the system.

## Includes everything to date
Driver-only settlement load picker, settlement PDF itemized fix, itemized
settlement lines, driver settlement detail, settlement layout fix, easy
driver-wage creation, rental truck swap, photo viewer signed-URL fix, truck photo
gallery, office PWA + mobile layout, phone tap-to-call/text + phone login +
SMS-ready, driver nav + stop status + scanner, dismissible location notice, driver
map coordinates, driver location tracking + live map, driver PWA app, driver load
detail, driver login fix, driver invite links, create-driver-login button, driver
portal, IFTA print, broker detail page, driver wages detail, wages on single-truck
report, per-truck driver-wage attribution, team invite + approval, per-truck P&L
expense fix, improved rate-con broker auto-add, vehicle cost % breakdown,
vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead fix +
auto-fill, chat + task files, notifications (bell+email) + task responses, chat
@mentions + chat-to-task, team username + remove, floating team chat + handoff,
duplicate rate-con protection, rate-con broker+agent auto-create, all-brokers list,
brokers + agents, admin-only delete, vehicle page fix, unified load form, vehicle
docs front, auto miles, vehicle photos, email document, hiring phases 1-6,
dashboard KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs,
company logins, FMCSA lookup.

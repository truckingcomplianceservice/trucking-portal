# Trucking Compliance Services — Operations Portal

Add ANY existing load to a settlement by clicking (not just manual entry).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What changed
Before, the "Add a load" picker on a settlement only listed loads ALREADY assigned
to that driver. So if a load wasn't assigned to them, you couldn't click to add it
-- you had to type it manually.

Now the picker shows ALL loads in the system that aren't already on a settlement:
- the driver's own loads,
- loads that were assigned to a different driver (shown as "(was Bob)"),
- and unassigned loads (shown as "(unassigned)").

Each option shows the date, reference, route, and rate. Click one, hit Add, and:
- it's attached to this settlement,
- and assigned to this driver (so the pay lines up),
- and it shows in "Loads covered" with its pickup date and amount.

You can still "Add a load manually" for a load that isn't in the system at all.

## Includes everything to date
Click-add existing loads to settlement, settlement PDF itemized fix, itemized
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

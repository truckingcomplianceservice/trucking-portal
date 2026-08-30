# Trucking Compliance Services — Operations Portal

FIX: settlement page right panel ("Mark as paid") was squished/cut off.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What was wrong (from your screenshot)
On the driver settlement page, the right-hand "Mark as paid" and "Edit amounts"
panel was being crushed into a tiny sliver and cut off at the edge of the screen,
and the "Add a load" button was chopped off too. The two-column layout wasn't
giving the right column enough room.

## The fix
- The right panel now has a guaranteed minimum width so it can't collapse.
- On smaller/medium screens the page now stacks into ONE column (settlement on
  top, "Mark as paid" + "Edit amounts" below) so nothing is ever cut off.
- Form fields are kept within the page width.

Everything on the page works the same -- this is purely fixing the squished/cut-off
layout you saw. You'll now be able to see and use "Mark as paid" (date, method,
reference), "Edit amounts", "Add a load", and the reimbursement fields properly.

## Includes everything to date
Settlement layout fix, easy driver-wage creation, rental truck swap, photo viewer
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

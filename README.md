# Trucking Compliance Services — Operations Portal

Makes creating driver wages easy to find (it was hard to locate before).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## The fix: it wasn't broken, it was hard to find
Driver wages/settlements worked, but there was no obvious "start here" button.
Now there are TWO clear ways:

WAY 1 -- from a driver's page (easiest):
  Drivers -> click the driver -> click "💵 Create wages / settlement" at the top.
  This instantly creates their settlement and opens it, where you can:
   - Add loads (pick from their loads, or add a manual load with a rate)
   - Set gross pay (use loads total, or a % of loads, or type it)
   - Add EXTRA REIMBURSEMENT to the driver
   - Subtract deductions
   - Mark it Paid (with date, method, reference)

WAY 2 -- from the sidebar:
  Sidebar -> "Driver pay" -> big "+ New driver wages" button at the top jumps you
  to the create form. Pick driver + week (or day, or per-load) -> "Create &
  review".

## Where you add loads & reimbursement (the part you couldn't find)
Both ways land you on the SETTLEMENT page. On that page:
- "Add a load..." dropdown = attach existing loads to this settlement.
- "Add manual load" = type a load # / rate by hand.
- "Extra reimbursement to driver ($)" field = reimburse tolls, etc.
- Net pay updates automatically = gross - deductions + reimbursement.

Nothing about the calculations changed -- this update is purely about making the
buttons easy to find.

## Includes everything to date
Easy driver-wage creation, rental truck swap, photo viewer signed-URL fix, truck
photo gallery, office PWA + mobile layout, phone tap-to-call/text + phone login +
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

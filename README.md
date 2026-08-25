# Trucking Compliance Services — Operations Portal

Rental swap: replace a broken-down truck, keep BOTH histories.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: rental truck swap (different VIN, same unit)
Scenario: Unit 1604 (rented) breaks down; the rental company sends a replacement
truck with a DIFFERENT VIN, and you keep calling it 1604. You want both trucks'
records kept cleanly.

HOW TO DO IT:
1. Go to the broken truck's page (Unit 1604).
2. Click "🔁 Replace this truck (rental swap)".
3. Enter the old truck's RETURN date, then the NEW truck's VIN (and plate/unit# --
   you can keep the same unit number 1604 or change it), and its in-service date.
4. Save. The system:
   - RETIRES the old truck (marks it Retired/returned with the return date) and
     keeps ALL its loads, expenses, and documents exactly as they are.
   - CREATES the new truck as its OWN record (own VIN = own clean history), linked
     to the one it replaced.

WHY THIS WAY (important): each physical truck (VIN) stays its own record, so your
P&L and history for the old truck and the new truck never get mixed. On each
truck's page you'll see the link: the new one says "replaced Unit 1604", the old
one says "replaced by ..." -- so you can follow the chain, but the numbers stay
clean and separate.

Retired trucks stay in the system (not deleted) so their history is always there.

## Includes everything to date
Rental truck swap, photo viewer signed-URL fix, truck photo gallery, office PWA +
mobile layout, phone tap-to-call/text + phone login + SMS-ready, driver nav + stop
status + scanner, dismissible location notice, driver map coordinates, driver
location tracking + live map, driver PWA app, driver load detail, driver login fix,
driver invite links, create-driver-login button, driver portal, IFTA print, broker
detail page, driver wages detail, wages on single-truck report, per-truck
driver-wage attribution, team invite + approval, per-truck P&L expense fix,
improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

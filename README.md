# Trucking Compliance Services — Operations Portal

Search loads by number when adding to a settlement.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: searchable load picker on settlements
When adding loads to a settlement, there's now a search box above the list:
"Type a load number to find it fast...". As you type, the list filters instantly
to matching loads -- by load number, origin, destination, or date. No scrolling
through a long list.

- The list shows as a scrollable box (6 rows visible) instead of a dropdown.
- Type a load number (or city/date) and only matching loads stay visible.
- The first match auto-selects, so you can type then click "Add" right away.
- A counter shows how many loads match your search.

Still only shows that driver's loads not already on a settlement (unchanged).

## Includes everything to date
Searchable load picker, settlement wage calculator, daily/per-load/percentage
settlements, driver-only load picker, settlement PDF itemized fix, itemized
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

# Trucking Compliance Services — Operations Portal

Check: the dollar amount position is now adjustable on its own.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## The fix: line up the amount with the $ sign yourself
Since every check stock is a little different, the dollar amount now has its OWN
adjustment so you can line it up perfectly with the $ sign without moving anything
else.

HOW TO USE:
1. Admin -> Companies -> your company.
2. Find "Amount box offset X" and "Amount box offset Y".
3. Print on plain paper, hold against a real check:
   - Amount too far LEFT of the $ sign?  -> increase Amount offset X (e.g. 6, 10)
   - Too far RIGHT?                        -> use a negative X (e.g. -6)
   - Sitting too LOW / under the line?     -> use a negative Y (e.g. -6, -10)
   - Too HIGH?                             -> use a positive Y
   (Units are points, about 1/72 inch each. Try 5-10 at a time.)
4. Reprint until the amount sits right next to the $ sign. Done once, it's set.

The check page shows the current amount offsets and a reminder of which way each
moves. This adjusts ONLY the amount; the whole-page Offset X/Y still moves
everything together.

## Includes everything to date
Adjustable check amount position, hide-load-amounts consistency, optional
hide-load-amounts on check, check amount alignment, owner-operator company pay +
EIN on 1099, driver "pay checks to" business name, IFTA CSV import, P&L partner
breakdown, partner statement, expense "Paid by" dropdown, partner ledger, loads on
check stub, LMP100 check layout, load photos gallery, driver check printing,
invoice load search, invoice auto-fill from load, P&L miles + $/mi, auto
loaded-miles, invoice unpaid-until-recorded, invoice custom line items + email,
searchable load picker, settlement wage calculator, daily/per-load/percentage
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

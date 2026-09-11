# Trucking Compliance Services — Operations Portal

IFTA: upload any CSV mileage/ELD report instead of typing state miles by hand.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Upload CSV / import mileage on the IFTA worksheet
On the IFTA page there's a new "Upload CSV / import mileage" button. Steps:
1. Upload any mileage or ELD CSV -- no specific template needed.
2. The system AUTO-DETECTS the state and miles columns even when providers use
   different names (State, Jurisdiction, Miles, Distance, Total Miles, Jurisdiction
   Miles, etc.). If it can't tell, it shows a mapping screen to pick the columns.
3. It recognizes states by full name OR abbreviation (California or CA), combines
   duplicate state rows, and totals miles per state.
4. IMPORT PREVIEW shows each state with miles (from CSV) and gallons (pulled
   automatically from your Fuel transactions for that quarter), e.g.:
     CA — 4,532 miles — 1,240 gallons
     NV — 1,820 miles — 410 gallons
     AZ — 2,104 miles — 530 gallons
5. Rows with an unrecognized state are shown as a warning and skipped.
6. Click "Import these miles" and the worksheet's Miles column is filled in. You can
   still review/edit miles and add tax rates, then Save & Recalculate as before.

All the IFTA math (total miles, total gallons, fleet MPG, taxable gallons, net
gallons, tax owed/credit) works exactly as before -- the import just fills the
miles for you instead of manual entry.

## Includes everything to date
IFTA CSV import, P&L partner breakdown, partner statement, expense "Paid by"
dropdown, partner ledger, loads on check stub, LMP100 check layout, load photos
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

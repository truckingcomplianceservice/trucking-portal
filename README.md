# Trucking Compliance Services — Operations Portal

Owner-operators: pay to their company + EIN, and 1099 goes to the company.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: pay a driver as their company (like a leased carrier)
On a driver's page, the "Pay checks to" card now has TWO fields:
- Business / company name on checks (e.g. Singh Trucking LLC)
- Business EIN (for 1099)

When BOTH the driver's checks and 1099 should go to their company:
- Set the business name -> checks are made out to the company.
- Set the business EIN -> the 1099-NEC is generated against the COMPANY NAME +
  EIN (not the personal name/SSN). Exactly how you'd 1099 a leased carrier, even
  though he's your driver.

If you leave the business name blank, everything works the old way: checks and the
1099 use the driver's personal name and their SSN/EIN in the Tax ID field.

The 1099 page now clearly shows "(paid as company)" and uses the EIN when the
driver is set up this way.

## Includes everything to date
Owner-operator company pay + EIN on 1099, driver "pay checks to" business name,
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

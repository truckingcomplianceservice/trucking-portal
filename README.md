# Trucking Compliance Services — Operations Portal

Print driver paychecks onto pre-printed check stock (works with your Canon MF240).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## One-time setup (Admin -> Companies -> your company)
- Bank name (for checks)
- Next check number (e.g. 1001)
- Signature line name (optional)
- Check print offset X / Y -- leave 0 for now; use these to nudge alignment later.

## How to print a driver check
1. Open the driver's settlement (Driver pay -> the settlement).
2. Click "Print check".
3. It shows a check laid out for a STANDARD business check on the TOP third of the
   page, filled with: payee (driver), $ amount, amount in words, date, and memo
   (the pay period). Check number is shown.
4. FIRST TIME: click "Print check" on PLAIN paper, hold it against your real check
   to see if the payee/amount/words line up. If they're off, set the X/Y offsets in
   Admin -> Companies (X: +right/-left, Y: +down/-up, in points ~1/72 inch) and
   reprint until it lines up. You only do this once per check stock.
5. Then load your pre-printed checks and print. Use "Assign next check #" to pull
   the next number and advance the counter.

## IMPORTANT honest notes
- This is for PRE-PRINTED check stock (your bank/printer already put your account
  info + the magnetic MICR line on them). Your Canon MF240 just adds the
  payee/amount/etc -- which it does fine with normal toner.
- Do NOT try to print the MICR line yourself on blank stock with the MF240 -- it
  can't do magnetic toner and banks may reject those checks.
- The default layout is the common "check-on-top" business format. If your check
  stock has the check in the MIDDLE or BOTTOM, tell me and I'll add that layout.

## Includes everything to date
Driver check printing (pre-printed stock), invoice load search, invoice auto-fill
from load, P&L miles + $/mi, auto loaded-miles, invoice unpaid-until-recorded,
invoice custom line items + email, searchable load picker, settlement wage
calculator, daily/per-load/percentage settlements, driver-only load picker,
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

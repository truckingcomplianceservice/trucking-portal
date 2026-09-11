# Trucking Compliance Services — Operations Portal

Per-partner statement: itemized history of what they spent and got paid back.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: partner statement (like a bank statement)
On the Partners page, CLICK a partner's name to open their full statement:
- Totals up top: total contributed, total paid back, still owed.
- TRANSACTION HISTORY in date order: every out-of-pocket expense they paid (In)
  and every payback (Out), each with a description and date, plus a RUNNING BALANCE
  owed after each line.
- Print or Download PDF.

Example (Muzammal spends $400, paid back in two parts):
  Aug 1   Truck repair (Unit 101)   + $400            Balance $400
  Aug 10  Payback — Zelle                    - $150   Balance $250
  Aug 20  Payback — Check                    - $250   Balance $0
So you can see exactly how much he spent, how much he's been paid back, and what's
still owed at any point -- and hand him a printed statement.

## Full flow recap
1. He spends money -> add expense, "Paid by: Partner [name]" -> shows as his
   contribution.
2. Company pays him -> Partners page -> "Record a payback".
3. His statement + the ledger show contributed, paid back, and still owed, per
   partner and per truck.

## Includes everything to date
Partner statement (itemized + PDF), expense "Paid by" dropdown, partner ledger,
loads on check stub, LMP100 check layout, load photos gallery, driver check
printing, invoice load search, invoice auto-fill from load, P&L miles + $/mi, auto
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

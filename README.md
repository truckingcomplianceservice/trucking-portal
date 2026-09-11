# Trucking Compliance Services — Operations Portal

Profit & Loss now includes partner spending, balances, and profit distribution.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New on the Profit & Loss report (Reports -> Profit & Loss)
Below the usual P&L (revenue, expenses, wages, miles, net) there's now a
"Partner breakdown & profit distribution" section. For each company it shows:
- The company's NET PROFIT/LOSS.
- A row per partner:
  * Ownership %
  * Spent (out of pocket) -- what that partner paid from their pocket
  * Paid back -- what the company has returned to them
  * Still owed -- what the company still owes them (spent - paid back)
  * Profit share -- ownership % x net profit (their slice of the profit)

So the P&L now answers all of it in one place: profit/loss of the company, how
much each partner spent, how much is still owed to each, and how the profit
divides between the partners.

Example (2 partners 50/50, $8,000 net profit; Muzammal spent $400, paid back $150):
  Muzammal  50%  spent $400  paid back $150  still owed $250  profit share $4,000
  Ali       50%  spent $0    paid back $0    still owed $0    profit share $4,000

NOTE: "Profit share" (each partner's slice of profit) and "Still owed" (cash to
return for out-of-pocket spending) are separate on purpose -- one is equity
earnings, the other is a reimbursement. Keep ownership % totaling 100%.

## Includes everything to date
P&L partner breakdown + profit distribution, partner statement, expense "Paid by"
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

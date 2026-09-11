# Trucking Compliance Services — Operations Portal

Partner ledger: track what each partner puts in, gets back, owns, and earns.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## Setup (one time)
Admin -> Partners -> Add a partner for each owner: name + ownership % (e.g. 50 and
50). Do this per company if partners differ by company.

## How it works (Sidebar -> Partners)
COMPANY-WIDE table, per partner:
- Ownership %
- Contributed = out-of-pocket expenses that partner paid
- Paid back = money returned to them
- Still owed = contributed - paid back (red if the company still owes them)
- Profit share = ownership % x company profit (revenue - expenses - wages)

PER-TRUCK breakdown: for each truck, how much each partner contributed / was paid
back / is still owed on that specific truck.

## How to record the money
- PARTNER PAID AN EXPENSE: Accounting -> add expense -> check "out of pocket" and
  set "paid by partner". It shows as that partner's contribution (and if you set a
  truck on the expense, it shows under that truck too).
- PARTNER GOT PAID BACK: Partners page -> "Record a payback" -> pick partner,
  amount, optional truck, method. It reduces what they're owed.

So you can always answer: how much has each partner put in, how much have we paid
them back, how much do we still owe them, and what's their profit share -- overall
and per truck.

## Includes everything to date
Partner ledger (contributions/paybacks/ownership/profit split, per truck), loads on
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

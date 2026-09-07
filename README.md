# Trucking Compliance Services — Operations Portal

Invoice stays UNPAID until a payment is recorded (sending never marks it paid).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this clarifies
An invoice's paid/unpaid status is driven ONLY by recorded payments:
- New invoice = UNPAID.
- Emailing or printing an invoice does NOT change the status (it stays UNPAID).
- It becomes PARTIALLY PAID when a partial payment is recorded, and PAID only when
  payments cover the full total.

So the dispatcher/biller controls it: when the customer actually pays, they open
the invoice and "Record a payment" (or click "Mark fully paid" for the whole
balance in one click). Until then it stays UNPAID no matter how many times it's
sent.

The invoice now shows a clear UNPAID / PARTIALLY PAID / PAID badge and a note
explaining that sending never marks it paid.

## Includes everything to date
Invoice unpaid-until-recorded + clearer status, invoice custom line items + email,
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

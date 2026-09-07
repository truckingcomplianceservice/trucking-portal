# Trucking Compliance Services — Operations Portal

Invoices: custom line items + email straight to the customer.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New 1: custom line items on invoices
Open an invoice (Billing -> the invoice). There's a new "Line items (custom
charges)" box. Add as many charges as you want, each with a description, quantity,
and unit price -- e.g.:
  Line haul Dallas->Miami   1 x $2,000 = $2,000
  Detention                 2 x $75    = $150
  Lumper fee                1 x $90    = $90
The lines add up to the invoice subtotal automatically, and the total (minus
discount, plus tax) updates. Remove any line with the x button. They show on the
printed/emailed PDF too.

(If you add no line items, the invoice still works the old way with a single
subtotal.)

## New 2: email the invoice to the customer
On the invoice, click "Email to customer". Enter the customer's email (pre-filled
from the broker's email if it's saved), add an optional message, and Send. The
system emails them the invoice as a PDF attachment, from your company email.

## Includes everything to date
Invoice custom line items + email, searchable load picker, settlement wage
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

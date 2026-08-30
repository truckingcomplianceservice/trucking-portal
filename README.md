# Trucking Compliance Services — Operations Portal

Itemized deductions & reimbursements with descriptions (add as many as you want).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: itemized lines with descriptions
On a settlement (Driver pay -> open a settlement), there's a new
"Itemized deductions & reimbursements" box. You can add AS MANY lines as you want,
each with:
- Type: Reimbursement (adds to pay) or Deduction (subtracts from pay)
- Description: e.g. "Lumper fee at Miami", "Trailer rent", "Cash advance",
  "Detention pay"
- Amount

Each line shows in the pay breakdown (green + for reimbursements, red - for
deductions) and is included in the net pay automatically. Remove any line with the
× button.

THE DRIVER SEES IT TOO: in their app, when they open the settlement, each itemized
line shows with its description and amount -- so they know exactly what each
reimbursement and deduction is for.

You still have the simple single "Deductions" and "Extra reimbursement" fields for
quick totals; the itemized lines are for when you want to spell out each item.

## Includes everything to date
Itemized settlement lines, driver settlement detail, settlement layout fix, easy
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

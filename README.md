# Trucking Compliance Services — Operations Portal

Settlement wage calculator: %, per mile (with empty miles), per load, or total.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: "Calculate wages" panel on every settlement
After you add the loads to a settlement, use the new "Calculate wages" box. It
shows the loads count, loads total, loaded miles, empty (deadhead) miles, and
total miles -- then lets you set gross pay four ways:

1) BY PERCENTAGE -> gross = % x loads total (prefilled with the driver's % if set).
2) BY MILE -> gross = rate x miles. There's a checkbox "Include empty/deadhead
   miles" -- checked, it pays for loaded + empty miles; unchecked, loaded only.
   (Prefilled with the driver's per-mile rate if set.)
3) FLAT AMOUNT PER LOAD -> gross = amount x number of loads on the settlement.
4) FULL LOADS TOTAL -> gross = the loads' combined rate.

Pick whichever matches how you pay that driver; the gross updates instantly and
flows into net pay (after deductions/reimbursements). You can still type gross by
hand in "Edit amounts".

Example tested: 2 loads, $5,000 total, 2,500 loaded + 300 empty miles ->
  25% = $1,250 | $0.60/mi incl empty = $1,680 | $0.60/mi loaded = $1,500 |
  $500/load = $1,000 | full total = $5,000.

## Includes everything to date
Settlement wage calculator (% / per-mile+deadhead / per-load / total),
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

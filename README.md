# Trucking Compliance Services — Operations Portal

Added a Print button to IFTA (all other reports already print).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## Printing reports
Yes -- you can print your reports. Each report page has a "Print" button (top
right). Clicking it opens your browser/computer print dialog, where you can print
on paper OR "Save as PDF". The app automatically hides the sidebar, menus, and
buttons when printing, so you get a clean, professional printout.

Reports that print: Profit & Loss, Per-truck P&L, single-truck detail (also has a
dedicated Download PDF), driver report, tax, factoring, maintenance, compliance,
activity, report builder, and now IFTA (this update -- it was the only one missing
a Print button).

Tip: some reports (like a single truck's P&L) also have a "Download PDF" button
that makes a proper PDF file directly; "Print -> Save as PDF" works on any report.

## Includes everything to date
IFTA print button, broker detail page, driver wages detail, wages on single-truck
report, reports label fix, per-truck driver-wage attribution, team invite +
approval, per-truck P&L expense fix, improved rate-con broker auto-add, vehicle
cost % breakdown, vehicle-expense fix, IFTA worksheet, company switcher fix,
deadhead nearby-city fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

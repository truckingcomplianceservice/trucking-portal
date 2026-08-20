# Trucking Compliance Services — Operations Portal

Fix: the company switcher (top-right) now actually filters the page.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
The company dropdown at the top-right (next to Admin) wasn't working on several
pages -- picking a company did nothing. Cause: the Dashboard, Tax report,
Factoring report, and Activity feed used a helper that ignored the switcher and
always showed ALL companies.

Now when you pick a company up top, those pages correctly show ONLY that
company's data, and "All companies" shows everything. The choice sticks as you
move between pages.

## Includes everything to date
Company switcher fix, deadhead nearby-city fix + auto-fill, chat + task file
attachments, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

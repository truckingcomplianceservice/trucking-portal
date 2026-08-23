# Trucking Compliance Services — Operations Portal

FIX: drivers can now actually log in. Use the right login page.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## IMPORTANT: which login page to use
Drivers must log in at:   https://app.pure99inc.com/login/
NOT at the admin page (/admin/login/).

WHY: the /admin/ login only allows office "staff" users. Drivers are intentionally
NOT staff (so they can't reach admin/office pages) -- so the admin login correctly
refused them. That's why your driver couldn't get in even with the right password.

This build fixes it two ways:
- The app's main login is now /login/ (which accepts drivers AND office users).
- When a driver logs in there, they're sent straight to their driver portal.
- Office/admin users still land on the dashboard as before.
- You can still use /admin/ for the back-office admin (staff only).

So tell your drivers to go to app.pure99inc.com/login/ (or just app.pure99inc.com
-- anything that needs login now points to the driver-friendly page).

## Quick test
1. Create a driver login (Drivers -> driver -> Create driver login), or use one you
   made.
2. Open an incognito window -> go to https://app.pure99inc.com/login/
3. Log in as the driver -> you should land in the driver portal (/driver/).

## Includes everything to date
Driver login fix, driver invite links, create-driver-login button, driver portal,
IFTA print, broker detail page, driver wages detail, wages on single-truck report,
per-truck driver-wage attribution, team invite + approval, per-truck P&L expense
fix, improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense
fix, IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task
files, notifications (bell+email) + task responses, chat @mentions + chat-to-task,
team username + remove, floating team chat + handoff, duplicate rate-con
protection, rate-con broker+agent auto-create, all-brokers list, brokers + agents,
admin-only delete, vehicle page fix, unified load form, vehicle docs front, auto
miles, vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2
cloud backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

# Trucking Compliance Services — Operations Portal

One-click "Create driver login" button on each driver's page.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## How to give a driver access to the driver portal
1. Go to Drivers -> click the driver.
2. Scroll to the new "Driver portal login" card.
3. Enter a username and a password (min 8 chars) -> click "Create driver login".
4. Give that username + password to the driver (securely).
5. The driver goes to your site (app.pure99inc.com), logs in, and AUTOMATICALLY
   lands in the driver portal -- they never see your office/admin pages.

To see the portal yourself: create a login for a test driver, then log in as them
in an incognito window. The portal lives at /driver/.

Admins can also "Remove login" to disable a driver's access.

## What the driver sees (recap)
Their loads + history, upload BOL/POD, add expenses (with receipt photo), their
pay/settlements, and a notifications bell. They see the load RATE only if you turn
on Company -> "Drivers can see load rate ($)". They can only ever see their OWN
data.

## Coming next (your pick): driver self-signup by invite link
Like the team invite links -- you'd text a driver a link, they set their own
password, you approve. Say the word and I'll build it.

## Includes everything to date
Create-driver-login button, driver portal, IFTA print, broker detail page, driver
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

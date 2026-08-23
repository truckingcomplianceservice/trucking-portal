# Trucking Compliance Services — Operations Portal

DRIVER APP (PWA): drivers install the portal to their phone home screen.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: the driver portal is now an installable app (iPhone + Android)
Drivers get an APP ICON on their phone, and it opens FULL-SCREEN like a real app
-- no browser bars, no typing a web address. Works on both iPhone and Android.
Free, no app store needed.

## How a driver installs it (tell your drivers this)
ANDROID (Chrome):
1. Go to app.pure99inc.com/login/ and log in.
2. A banner "Install this app -> Add to home screen" appears -> tap it.
   (Or Chrome menu -> "Install app" / "Add to Home screen".)
3. An app icon appears on their phone. They tap it from now on.

IPHONE (Safari):
1. Go to app.pure99inc.com/login/ and log in.
2. Tap the Share button (square with an up-arrow) at the bottom.
3. Tap "Add to Home Screen".
4. An app icon appears. They tap it from now on -- opens full screen.

After install, the app opens straight to the driver portal. They log in once and
stay logged in (like any app). The app shows their loads, miles, documents
(BOL/POD/rate con if allowed), lets them upload POD, add expenses, and see pay.

NOTE: iPhone only allows install from SAFARI (not Chrome on iPhone). Android uses
Chrome. This is an Apple/Google rule, not our app.

## Later (optional): true App Store / Play Store version
Costs ~$99/yr (Apple) + $25 once (Google), weeks of setup, app review, and ongoing
maintenance. Worth it only when selling to many carriers. The PWA covers drivers'
needs now for free.

## Includes everything to date
Driver PWA (installable app), driver load detail (miles + docs), driver login fix,
driver invite links, create-driver-login button, driver portal, IFTA print, broker
detail page, driver wages detail, wages on single-truck report, per-truck
driver-wage attribution, team invite + approval, per-truck P&L expense fix,
improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

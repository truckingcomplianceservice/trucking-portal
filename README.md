# Trucking Compliance Services — Operations Portal

Office/admin is now an installable app + proper phone layout.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: install the OFFICE app on your phone (you + dispatchers)
Just like the driver app, but for the office side (dashboard, dispatch, loads,
drivers, brokers, reports, everything). You get an app icon and full screen.

ANDROID (Chrome): go to app.pure99inc.com/dashboard/ and log in -> Chrome menu ->
"Install app" / "Add to Home screen".
IPHONE (Safari): go to app.pure99inc.com/dashboard/ and log in -> Share button ->
"Add to Home Screen".

The office app icon is GOLD with "TCS OFFICE" (the driver app icon is navy "TCS")
so you can tell them apart if you install both.

## New: better phone layout
On a phone, the side menu now slides away so pages use the FULL width. Tap the
☰ menu button (top-left) to slide the menu in; tap a link or the dark area to
close it. Wide tables now scroll sideways instead of squishing. Everything you can
do on a laptop, you can now do from your phone comfortably.

## Note
This is the SAME login as always -- admins/dispatchers log in and get the office
app; drivers get the driver app automatically. Same accounts, same data.

## Includes everything to date
Office PWA + mobile layout, phone tap-to-call/text + phone login + SMS-ready,
driver nav + stop status + scanner, dismissible location notice, driver map
coordinates, driver location tracking + live map, driver PWA app, driver load
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

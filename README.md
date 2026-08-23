# Trucking Compliance Services — Operations Portal

Driver location tracking (phone GPS) + live map for admin & dispatchers.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: driver location tracking
- Turn it ON per company: Admin -> Companies -> your company ->
  "Track driver location (phone GPS)".
- When ON, the driver app shares the phone's location WHILE THE APP IS OPEN
  (the driver must tap "Allow" for location). The driver sees a clear green bar:
  "Location sharing is ON while this app is open" -- honest + consent-friendly.
- Location updates once on open and every 60 seconds while the app stays open.

## New: live driver map (you + dispatchers)
- Sidebar -> "Driver map" (visible to admins, managers, dispatchers, safety).
- Shows every driver sharing location on a map, with a list underneath:
  driver, company, last update time, and Live (green, seen in last 15 min) or
  Stale (red, older).
- Refreshes every 20 seconds. Uses a free map (OpenStreetMap) -- no API key.

## HONEST LIMITS (please read)
- This is PHONE tracking while the app is OPEN. Phones/browsers do NOT allow a web
  app to track location in the background or when locked -- especially iPhone. So
  this is great for "where is my driver now" check-ins, not silent 24/7 tracking.
- For true 24/7 background tracking, the reliable route is ELD INTEGRATION (your
  TRCeLog ELD already has the truck's GPS by law). That needs the ELD provider's
  API -- a good "later" step. The system is built so ELD can feed the same map.
- LEGAL: tracking people's location usually requires informing them (and often
  consent). The app shows drivers that tracking is on, which helps -- but for
  selling to other carriers, have your lawyer confirm your policy/consent wording.

## Includes everything to date
Driver location tracking + live map, driver PWA app, driver load detail, driver
login fix, driver invite links, create-driver-login button, driver portal, IFTA
print, broker detail page, driver wages detail, wages on single-truck report,
per-truck driver-wage attribution, team invite + approval, per-truck P&L expense
fix, improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense
fix, IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task
files, notifications (bell+email) + task responses, chat @mentions + chat-to-task,
team username + remove, floating team chat + handoff, duplicate rate-con
protection, rate-con broker+agent auto-create, all-brokers list, brokers + agents,
admin-only delete, vehicle page fix, unified load form, vehicle docs front, auto
miles, vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2
cloud backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

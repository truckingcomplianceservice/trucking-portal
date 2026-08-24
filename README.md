# Trucking Compliance Services — Operations Portal

Driver app upgrade: Navigate buttons, pickup/delivery status, BOL scanner.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New in the driver app (open any load)

1) NAVIGATE BUTTONS (pickup + delivery)
   Each load shows a Pickup card and a Delivery card, each with a "Navigate"
   button. Tapping it opens the phone's map with the address loaded. On the phone,
   the driver can choose Google Maps, Trucker Path, or ANY truck navigator they
   have installed -- so they get real truck routes. (We hand off to their nav; we
   don't replace it.)

2) STOP STATUS (this is your real-time data)
   Buttons: Arrived at pickup, Loaded, Arrived at delivery, Delivered. When the
   driver taps one, the app records the milestone WITH the time and their location
   at that moment, notifies you + dispatchers instantly, and moves the load's
   status forward (Loaded -> In transit, Delivered -> Delivered). A status history
   with timestamps + coordinates shows on the load. This gives brokers real answers
   ("picked up at 9:14am, delivered at 3:02pm") without needing 24/7 tracking.

3) DOCUMENT SCANNER
   "Take photo with camera" opens the phone camera to snap the BOL/POD directly.
   There's also an "attach saved file / PDF" option. Uploaded docs appear on the
   load for you and the driver, and you're notified on POD.

## Honest note on navigation
We do NOT build turn-by-turn truck navigation (that's what Trucker Path / Google
Maps do, with licensed map data + truck routing). The Navigate button launches
whichever of those the driver prefers -- the reliable, standard approach.

## Includes everything to date
Driver nav + stop status + scanner, dismissible location notice, driver map
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

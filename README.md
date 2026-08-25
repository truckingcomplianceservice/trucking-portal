# Trucking Compliance Services — Operations Portal

REAL FIX #2: photo viewer "could not be loaded" (signed R2 URL escaping).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What was wrong (the honest, final cause)
Your photos live in Cloudflare R2 and are served via signed links that contain
special characters (& and =). In a normal <img> tag those work fine (that's why
thumbnails showed). But when those links were placed inside the photo viewer's
JavaScript list, the & was being turned into "&amp;", which corrupted the link --
so R2 refused it and you saw "could not be loaded".

Fixed by escaping the links correctly for JavaScript (so the & and = survive
intact). The viewer now loads the real full-size photos.

## Test after deploying
Open a truck with 2+ photos -> tap one -> the FULL photo shows (no dot, no error)
-> flip with ‹ › / swipe / arrow keys -> × or ESC to close.

If for any reason a photo still won't load, the most likely remaining cause would
be the 1-hour signed-link expiry -- just refresh the page to get fresh links. (In
normal use you'll always be opening fresh links, so this shouldn't happen.)

## Includes everything to date
Photo viewer signed-URL fix, truck photo gallery, office PWA + mobile layout,
phone tap-to-call/text + phone login + SMS-ready, driver nav + stop status +
scanner, dismissible location notice, driver map coordinates, driver location
tracking + live map, driver PWA app, driver load detail, driver login fix, driver
invite links, create-driver-login button, driver portal, IFTA print, broker detail
page, driver wages detail, wages on single-truck report, per-truck driver-wage
attribution, team invite + approval, per-truck P&L expense fix, improved rate-con
broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet,
company switcher fix, deadhead fix + auto-fill, chat + task files, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

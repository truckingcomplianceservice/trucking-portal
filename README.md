# Trucking Compliance Services — Operations Portal

Auto deadhead (empty) miles + Google Maps support (exact miles when key added).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: automatic deadhead (empty) miles
On the Add Load page, next to "Deadhead (empty) miles" there's now an "auto"
link. It finds the driver's (or truck's) PREVIOUS load's drop-off location and
measures the empty miles from there to THIS load's pickup. Steps:
  1) enter this load's pickup stop, 2) pick the driver or truck, 3) click "auto".
You can always edit the number. If there's no previous load, it tells you to
enter it manually.

## New: Google Maps for EXACT miles (optional)
Both loaded-miles and deadhead now use exact Google road miles IF a Google key is
set; otherwise they use the free estimate (unchanged). To turn on exact miles:
  1) Create a Google Cloud account (console.cloud.google.com), enable the
     "Directions API".
  2) Create an API key.
  3) In Railway -> web service -> Variables, add:
        GOOGLE_MAPS_API_KEY = (your key)
     Save; Railway redeploys.
That's it -- miles become exact automatically, no rebuild needed. Google has a
free monthly credit ($200) that typically covers normal fleet volume, but it
does require a card on file. Without the key, the free estimate keeps working.

## Includes everything to date
Auto deadhead + Google-ready miles, unified load form, vehicle docs front, auto
loaded miles, vehicle photos, email document, hiring phases 1-6, dashboard KPIs,
professional 1099, R2 cloud backup, multi-stop load, truck P&L date fix,
12-test suite, factoring, doc viewer, company docs, company logins, FMCSA lookup.

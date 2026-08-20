# Trucking Compliance Services — Operations Portal

Fix: deadhead now auto-fills + correctly handles nearby cities (e.g. Reno->Sparks).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
Your example: Load 1 Sacramento -> Reno, then Load 2 pickup Sparks, NV. The empty
(deadhead) miles should be Reno -> Sparks (~5 miles).

1. BUG FIXED: "Sparks, NV" (and many other cities) weren't in the list, so the app
   guessed the STATE CENTER and gave a wildly wrong number (206 miles instead of
   ~4). Added Sparks and dozens more CA/NV/OR/WA/TX freight cities. Reno->Sparks
   now correctly shows ~4 miles.
2. AUTO-FILL: deadhead now fills in automatically as soon as you pick the driver
   or truck (as long as you've entered the pickup and haven't typed a number
   yourself). You'll see a small green note showing the estimate and where it
   measured from. You can still click "auto" for a detailed popup, and always edit.
3. HONEST WARNING: if a city isn't recognized (only the state is), it now clearly
   says "rough estimate - check it" instead of giving a confident wrong number.

REMINDER: for the deadhead to find the previous drop, Load 1 must already be saved
with that same driver/truck and have a delivery date. For exact miles, add a
Google Maps key (GOOGLE_MAPS_API_KEY in Railway).

## Includes everything to date
Deadhead nearby-city fix + auto-fill, chat + task file attachments, notifications
(bell+email) + task responses, chat @mentions + chat-to-task, team username +
remove, floating team chat + handoff, duplicate rate-con protection, rate-con
broker+agent auto-create, all-brokers list, brokers + agents, admin-only delete,
vehicle page fix, unified load form, vehicle docs front, auto miles, vehicle
photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

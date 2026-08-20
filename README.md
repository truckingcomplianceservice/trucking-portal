# Trucking Compliance Services — Operations Portal

Duplicate rate confirmations are now blocked (no more double loads).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new: duplicate protection
When you create a load from a rate confirmation, the app now checks two things
before adding it:
1. FILE FINGERPRINT - if the exact same PDF was already uploaded for this
   company (even if you rename the file), it will NOT be added again. It shows a
   message and takes you to the existing load.
2. REFERENCE NUMBER - if a load with the same reference # already exists for this
   company, it's treated as a duplicate and not added again.

This prevents accidental double loads (which would have inflated your load count
and revenue). Each company is independent -- the same file can exist for a
different company if needed.

## Includes everything to date
Duplicate rate-con protection, rate-con broker+agent auto-create, all-brokers
list, brokers + agents, team messages, admin-only delete, vehicle page fix,
deadhead fix + Google-ready miles, unified load form, vehicle docs front, auto
miles, vehicle photos, email document, hiring phases 1-6, dashboard KPIs,
professional 1099, R2 cloud backup, 12-test suite, factoring, company docs,
company logins, FMCSA lookup.

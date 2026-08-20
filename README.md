# Trucking Compliance Services — Operations Portal

Team page: show usernames + add a Remove (delete) button.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
1. USERNAME NOW SHOWS: each team member's row now shows their @username (needed
   for login), alongside their name and email. Before, if someone had a name and
   email set, the username was hidden.
2. REMOVE A TEAM MEMBER: there's now a red "Remove" button next to each member
   (in addition to Deactivate). Rules:
   - Only the OWNER/admins can Remove (dispatchers/others cannot).
   - You cannot remove your own account.
   - The owner account cannot be removed.
   - It asks for confirmation, and suggests Deactivate if the person may return.

Deactivate = keeps the record but blocks login (good if they might come back).
Remove = permanently deletes the user account (use when they're gone for good).

## Includes everything to date
Team username + remove, floating team chat + handoff, duplicate rate-con
protection, rate-con broker+agent auto-create, all-brokers list, brokers + agents,
team messages, admin-only delete, vehicle page fix, deadhead fix + Google-ready
miles, unified load form, vehicle docs front, auto miles, vehicle photos, email
document, hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

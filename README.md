# Trucking Compliance Services — Operations Portal

Internal team communication (company-private): message board + notes on records.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Team messages (sidebar -> "Team messages")
- A simple company-PRIVATE message board. Team members post messages the rest of
  their company can see. Messages NEVER cross between companies (Pure 99 team
  can't see Roundway's, etc.). The owner sees the active company's board.
- Notes on records: an internal note can be attached to a load, driver, or
  applicant (also company-scoped). (The "Add note" box can be placed on those
  pages -- tell me where you want it and I'll wire the box in; the backend is
  ready now.)
- Delete rule: you can delete your own message; admins/owner can delete any.

Available to every role (dispatcher, compliance, accountant, etc.) so the whole
team can communicate -- but always within their own company only.

PRIVACY TESTED: company A cannot see, post to, or delete company B's messages or
notes (verified with two separate company logins).

## Includes everything to date
Team messages, admin-only delete, vehicle page fix, deadhead fix + Google-ready
miles, unified load form, vehicle docs front, auto miles, vehicle photos, email
document, hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup,
12-test suite, factoring, company docs, company logins, FMCSA lookup.

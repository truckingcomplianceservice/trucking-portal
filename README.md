# Trucking Compliance Services — Operations Portal

Hiring PHASE 6 — Audit center (export packages + expiring auditor links).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## PHASE 6 — Audit center (sidebar -> Audit center)
- Export a driver's DQF as a printable Audit Summary PDF (checklist status +
  signature audit records).
- Create a secure, EXPIRING, READ-ONLY auditor link (per driver or whole
  company) that an outside auditor opens WITHOUT a login. Every view is logged
  (count + last-viewed). Revoke any link instantly; revoked/expired links show
  a friendly "no longer active" page.

## Hiring module so far (Phases 1-6)
1 Recruiting pipeline · 2 DQF checklist · 3 Document review queue ·
4 E-signature audit trail · 5 Compliance center · 6 Audit center.

## Remaining: Phase 7 MVR/PSP/Clearinghouse provider interfaces -- these will be
built in SANDBOX/MOCK mode and cannot go live until you have vendor contracts +
API credentials. Legal review still required before any compliance claim.

## Includes everything to date
Hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup, multi-stop
load, truck P&L date fix, 12-test suite, factoring, doc viewer, company docs,
company logins, FMCSA lookup.

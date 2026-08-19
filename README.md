# Trucking Compliance Services — Operations Portal

Hiring PHASES 1-5: pipeline + DQF + doc review + e-signature audit + compliance center.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new since Phase 1-3

PHASE 4 — Electronic signature audit trail
When an applicant signs and submits the application, the system records an
immutable signature audit entry: signer name, timestamp, IP address, device/
browser, form name + version, and a SHA-256 content hash. Shown on the
applicant's profile under "Signature audit". NOTE: mechanics only -- not
certified legally compliant until reviewed by an attorney (ESIGN/UETA/FCRA).

PHASE 5/6 — Compliance center (sidebar -> Compliance center)
Whole-fleet compliance at a glance: compliant / warning / incomplete driver
counts, pending document reviews, open applicants, and documents expiring within
3, 7, 14, 30, 60, 90 days plus already-expired. Links straight to each driver's
DQF and the review queue.

## Still to come: Phase 6 audit-export package + expiring auditor links; Phase 7
MVR/PSP/Clearinghouse provider interfaces (sandbox until you have vendor
credentials + contracts). Legal review required before any compliance claim.

## Includes everything to date
Hiring phases 1-5, dashboard KPIs, professional 1099, R2 cloud backup, multi-stop
load, truck P&L date fix, 12-test suite, factoring, doc viewer, company docs,
company logins, FMCSA lookup.

# Trucking Compliance Services — Operations Portal

Hiring PHASE 1: full recruiting pipeline (build toward a DQF/compliance system).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## Hiring pipeline (sidebar -> Hiring)
Full applicant pipeline with stages: Invited, Application started, Incomplete,
Submitted, Pending review, Background checks pending, Documents missing,
Qualified, Approved for hire, Rejected, Active driver, Inactive, Archived.

On the pipeline board:
- Search applicants by name, email, phone, or tag.
- Each card shows a completion % bar and assigned recruiter + tags.
- "Show all stages" toggles the full set incl. archived/inactive.

Click an applicant to open their profile, where you can:
- See details, uploaded files, missing items, and completion %.
- Move them through pipeline stages (with a reason for approve/reject).
- Assign a recruiter.
- Add tags and internal notes (timestamped).
- View full status history (who changed what, when).
- Convert an approved applicant into an ACTIVE DRIVER in one click -- no
  duplicate data entry (name, contact, CDL carry over).

Company isolation enforced: each company login sees only its own applicants
(tested, incl. blocking direct-URL access to another company's applicant).

## What's next (later phases, from your spec)
Phase 2 DQF checklist per driver; Phase 3 document review queue + versioning;
Phase 4 expanded application + e-signature audit trail; Phase 5 automation/
reminders; Phase 6 audit center; Phase 7 MVR/PSP/Clearinghouse provider
interfaces (sandbox until you have vendor credentials). Legal sign-off needed
before calling anything ESIGN/FCRA/DPPA compliant.

## Includes everything to date
Hiring pipeline, dashboard KPIs, professional 1099, R2 cloud backup, multi-stop
load, truck P&L date fix, test suite (12 tests), factoring, doc viewer, company
docs, company logins, FMCSA lookup.

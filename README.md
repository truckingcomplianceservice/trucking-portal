# Trucking Operations Portal

Multi-company operations: companies, drivers, vehicles, loads (with BOL/POD &
factoring), expenses, settlements, P&L, online driver hiring, and compliance
document-expiry tracking. Django app on Railway.

## Deploying an update

Same repo, so Railway redeploys automatically:
1. In your `trucking-portal` GitHub repo: **Add file -> Upload files**.
2. Unzip this download and drag in ALL the contents (overwrites changed files).
3. Commit. Railway redeploys on its own.

No new Railway steps this time (the media volume from Phase 2 already handles
the applicant & compliance file uploads).

## Phase 3 — what's new

### Online driver hiring
- Each company has a unique, private application link. Find them at:
  **`your-app.up.railway.app/hiring/links/`** (copy button included).
- Send a link to a driver. They fill out the application and upload their CDL,
  medical certificate, etc. from their phone — no login needed.
- New applications appear under **Applicants** in the admin.
- Select applicants and use the **"Hire"** action to create their driver record
  and open a DQ file automatically, or **"Decline"**.

### Compliance & expiry tracking
- **Compliance documents** — add DQ-file documents per driver (application, MVR,
  medical, Clearinghouse, drug test, ELDT, etc.) each with an expiry date.
- Live dashboard at **`your-app.up.railway.app/reports/compliance/`** shows
  everything **overdue** and **expiring within 30 days** — pulling from driver
  CDL/medical dates, vehicle inspections, and compliance documents.

### Handy links
- P&L: `/reports/pnl/`
- Compliance: `/reports/compliance/`
- Hiring links: `/hiring/links/`

# Trucking Operations Portal

Full multi-company TMS: companies, drivers, vehicles, loads (documents +
factoring), expenses, settlements, P&L, online hiring, compliance tracking,
tax & 1099s, and activity/notifications. Django on Railway.

## Deploying an update
1. In your `trucking-portal` GitHub repo: **Add file -> Upload files**.
2. Unzip this download and drag in ALL the contents (overwrites changed files).
3. Commit. Railway redeploys on its own. No new Railway steps required.

## Phase 4 — what's new

### One place for everything: /reports/
Visit **`app.pure99inc.com/reports/`** for a menu linking to every report.

### Tax & 1099s  (/reports/tax/)
- Per-company income & expense totals for any year.
- 1099-NEC contractors listed with year-to-date pay and a $600 flag.
- Click **Generate 1099** for a printable 1099-NEC summary (Print / Save as PDF)
  to hand to your accountant or enter into an e-file service.
- Add your **EIN + address** on each Company, and a **Tax ID + address** on each
  1099 driver (new fields) so the 1099 is complete.

### Factoring  (/reports/factoring/)
- Outstanding invoices per company/factor (RTS / Bobtail), with totals.
  Closed loads are hidden so you see only what's awaiting payment.

### Notifications & activity
- **Activity feed** (/reports/activity/) — a running log: loads booked, payment
  changes, new applications, expenses, settlements.
- **Notification rules** (in the admin) — toggle, per event, whether it shows
  in-app / emails you / texts you. Text is a later add.
- **Email (optional):** to turn on email alerts, set `EMAIL_HOST`,
  `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (and optionally `DEFAULT_FROM_EMAIL`)
  in Railway Variables. Until then, notifications stay in-app (no errors).

### All report links
/reports/ · /reports/pnl/ · /reports/tax/ · /reports/factoring/ ·
/reports/compliance/ · /reports/activity/ · /hiring/links/

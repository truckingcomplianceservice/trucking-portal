# Trucking Compliance Services — Operations Portal

Adds a fleet-wide maintenance report.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents (including operations/static/logo.png).
3. Commit. Railway redeploys automatically.

## New: Fleet maintenance report
Vehicles -> **Maintenance report** (or /reports/maintenance/):
- Totals: this month, this year, total (filtered), and parts vs labor split.
- **Spend by vehicle** — every truck ranked by total maintenance cost, with
  record count and parts/labor breakdown.
- **Spend by month** — fleet-wide monthly totals.
- **Date-range filter**, **Print**, and **Download PDF** (with company letterhead).

Respects the company switcher: with one company active it shows that fleet;
with all companies it totals across them.

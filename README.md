# Fleetline — Trucking Operations Portal

Full multi-company TMS with a branded dashboard, operations, hiring, compliance,
factoring, tax/1099s, and notifications. Django on Railway.

## Deploying this update (Phase 5 — polish)
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents (overwrites changed files).
3. Commit. Railway redeploys automatically. No new Railway steps.

## Phase 5 — what's new (the polish layer)

### Branded dashboard (the new front door)
- Visiting **app.pure99inc.com** now opens a clean **Fleetline dashboard**, not
  the raw admin. It shows live KPIs (active loads, drivers, outstanding factoring,
  document alerts), quick-action buttons, recent loads, expiring documents, and a
  recent-activity feed — all pulled from your real data.
- A top navigation bar links to Loads, Drivers, Applicants, and Reports.

### Rebranded interface
- The whole admin is restyled in Fleetline's navy + amber with the logo, so every
  screen your team uses looks like a real product instead of a default backend.

Your team can start here: **app.pure99inc.com** (they log in, land on the dashboard).

## Note on further polish
This makes the app presentable and team-ready. Individual screens (e.g. a custom
drag-and-drop load board, driver self-service views) can be rebuilt as bespoke
custom pages later, one at a time, on top of this same foundation.

# Trucking Compliance Services — Operations Portal

Adds an all-companies portfolio command center (multi-client).

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents.
3. Commit. Railway redeploys automatically.

## New: All companies (portfolio)
For anyone with access to more than one company, a new **All companies** item
appears at the top of the sidebar. It shows every company as a scorecard:
- Active loads, drivers, trucks
- Outstanding AR, amount with factor
- Compliance alerts (expiring docs) — red if any need attention
- Totals across the whole portfolio at the top
Click a company to drop into its dashboard.

## How multi-client access works (already built)
- Add each client as a **Company** (Companies -> Add company). Add up to as many
  as you like.
- Add each client's login on the **Team** page and assign them ONLY their company.
  They see only their own loads, drivers, compliance, billing — nothing else.
- You (owner/admin) are assigned to all companies, so you see the portfolio and
  can drill into any client.
- Single-company clients don't see the "All companies" view at all — they just
  see their own dashboard.

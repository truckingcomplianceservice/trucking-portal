# Trucking Compliance Services — Operations Portal (COMPLETE)

Stage 1 of client portals: branded per-company login URLs.

## Deploy (one upload — this zip has everything)
1. Unzip -> copy ALL contents into your trucking-portal folder -> Replace all.
2. GitHub Desktop -> Commit -> Push -> wait for Railway "Successful".

## New: branded per-company portal link
Each company now has a portal URL: app.pure99inc.com/c/<slug>/
- The login page shows THAT company's logo and name (feels like their own portal).
- After login, the user lands inside that company automatically.
- Client users assigned only to that company still see only their company.
- Inside the app, the sidebar shows the active company's logo too.

### Set a short, clean link
A slug is auto-created from the name (e.g. "roundway-transport-llc"). To make it
short like /c/roundway:
  Admin -> Companies -> open the company -> Slug -> type "roundway" -> Save.
Then share: app.pure99inc.com/c/roundway

There's also a generic /login/ page with the shared Trucking Compliance branding.

## Note
This is Stage 1 (branding + convenience). Access is still enforced by each user's
account + company assignment — the pretty URL is a front door, not the lock.
Stage 2 (cross-tenant admin tier) and Stage 3 (subdomains, self-serve signup,
billing) are separate, larger steps.

## Includes everything to date
Branded portal login, role-based access, per-truck P&L, per-company logos,
background email, email 465/SSL, load filters, team edit/reset/invite, fuel
fixes + dedup, expense fix, portfolio, factoring aging, maintenance, DQF, billing.

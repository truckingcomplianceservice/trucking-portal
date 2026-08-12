# Trucking Compliance Services — Operations Portal (COMPLETE)

Complete current app. Fixes the "saving a load hangs" problem and everything prior.

## Deploy (one upload — this zip has everything)
1. Unzip COMPLETE-trucking-portal-LATEST.zip
2. Copy ALL contents into your trucking-portal folder -> Replace all
3. GitHub Desktop -> Commit -> Push -> wait for Railway "Successful"

## The save-hang fix
When a load's payment status changed, the app sent a notification email. With the
email variables set to port 465 on the old code (no timeout), that connection hung
and the Save spun forever. Now:
- Notification emails send in the BACKGROUND — saving a load/expense is never
  delayed by email, even if the mail server is slow or misconfigured.
- Email uses the right security automatically (465=SSL, 587=TLS) with a 20s timeout.

## Includes everything to date
Email 465/SSL support, load filters + status tabs, team edit/reset/invite,
fuel fixes (self-contained import, correct amount detection, right-company default,
duplicate protection, edit/delete), expense-upload fix, portfolio, factoring aging,
maintenance, DQF, billing + aging, letterheads.

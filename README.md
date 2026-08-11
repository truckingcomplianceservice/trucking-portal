# Trucking Compliance Services — Operations Portal

Fix: fuel CSV import 500 error + missing amount.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents.
3. Commit. Railway redeploys automatically.

## What was wrong
The fuel import's column-mapping step relied on two extra files (a templatetags
folder and a small partial template). If those didn't upload, the page threw a
500 and the amount never imported.

## Fixed
The fuel import is now **self-contained** — it needs only the main view and one
template, so a missed file can't break it. The confirm-columns step still lets you
map the Amount column correctly, and totals import as expected.

IMPORTANT: to be safe, upload ALL contents of this zip (the whole operations/
and templates/ folders), not just changed files.

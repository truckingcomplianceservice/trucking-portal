# Trucking Compliance Services — Operations Portal

Bugfix: expense file upload (Server Error 500).

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents.
3. Commit. Railway redeploys automatically.

## What was wrong
Saving an expense (with or without a receipt) threw a 500 error. The Expense
name-builder still referenced the old fixed category list after category was
changed to free-text, so Django crashed while logging the save.

## Fixed
- Expenses now save correctly, with or without a receipt attached.
- Custom (typed) expense categories work.
- Also fixed uploaded-file viewing in production (receipts/BOL/POD now open
  properly): corrected MEDIA_URL and added a media file route.

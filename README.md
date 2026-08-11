# Trucking Compliance Services — Operations Portal

Makes per-contractor 1099 actions obvious.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents.
3. Commit. Railway redeploys automatically.

## Change: 1099 per contractor
On the **Tax & 1099s** page, every 1099 contractor row now has three buttons:
- **Open / Print** — the printable 1099 (Print or Save as PDF).
- **PDF** — download that contractor's 1099 PDF directly.
- **Email** — opens the 1099 with the email form ready (sends the PDF once your
  email is connected in Railway).

These now appear for EVERY 1099 contractor (not only those over $600), so you can
generate, download, print, or email each one separately. The >= $600 threshold is
still shown as a status so you know who legally requires a 1099.

To see a contractor here: set the driver's tax status to "1099 contractor" and
record their settlement pay for the year.

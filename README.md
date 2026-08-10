# Trucking Compliance Services — Operations Portal

Adds printable reports everywhere, a real 1099 PDF, and emailing the 1099.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents (including operations/static/logo.png
   and the updated requirements.txt).
3. Commit. Railway redeploys automatically (it installs the new PDF library).

## New

### Print any report, anytime
Every report (P&L, Tax, Factoring, Compliance, Activity, Report Builder, Billing)
now has a **Print / Save as PDF** button. It prints a clean layout — sidebar and
buttons are hidden, just the data.

### 1099 as a real PDF
On Tax -> Generate 1099 you now have:
- **Download PDF** — a proper PDF file (not just browser print).
- **Print** — clean printout.

### Email the 1099 to anyone
- Click **Email this 1099**, enter a recipient (e.g. your accountant) and an
  optional message, and the app emails the **1099 PDF as an attachment**.
- This sends **once your email is connected**. Until then it shows a friendly
  note. To turn it on, add EMAIL_HOST / EMAIL_HOST_USER / EMAIL_HOST_PASSWORD
  (and DEFAULT_FROM_EMAIL) in Railway Variables.

## Email setup (to enable sending)
Easiest is Gmail with an App Password, or a service like Resend/SendGrid.
Add these Railway Variables on the web service:
- EMAIL_HOST (e.g. smtp.gmail.com)
- EMAIL_HOST_USER (your email address)
- EMAIL_HOST_PASSWORD (app password / API key)
- DEFAULT_FROM_EMAIL (the from address)
Then emailing works everywhere in the app.

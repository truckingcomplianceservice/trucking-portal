# Trucking Operations Portal

Companies, drivers, vehicles, loads, expenses, driver settlements, load
documents (BOL/POD), and a live Profit & Loss report per company.
Django app, deploys on Railway.

## Deploying an update (Phase 2)

You're replacing the code in your existing repo, so Railway redeploys automatically.

1. In your `trucking-portal` GitHub repo, click **Add file -> Upload files**.
2. Unzip this download and drag in ALL the contents (overwrites the changed files).
3. Commit. Railway sees the change and redeploys on its own.

## One new step: persistent file storage (for BOL/POD/receipts)

Uploaded files need a permanent home, or they vanish on each redeploy. Add a
Railway volume:

1. In Railway, click the **web** service -> **Settings** -> **Volumes** (or **+ Volume**).
2. Create a volume and set the **mount path** to:  `/app/media`
3. Go to **Variables** and add:  `MEDIA_DIR` = `/app/media`
4. Deploy. Uploaded documents now persist across every future deploy.

(If you skip this for now, the app still works — files just won't survive a redeploy. Add the volume before you rely on stored documents.)

## Using Phase 2

- **Loads** now have a "Documents & billing" section: invoice number, BOL, POD, rate con.
- **Expenses** — log fuel, maintenance, tolls, etc., linked to a company/driver/truck/load.
- **Settlements** — driver wages per period (net = gross − deductions).
- **Profit & Loss** — visit **/reports/pnl/** on your site for revenue − expenses −
  wages, per company and combined. (e.g. `your-app.up.railway.app/reports/pnl/`)

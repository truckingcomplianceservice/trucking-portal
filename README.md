# Fleetline — Trucking Operations Portal

Custom multi-company TMS with Brokers and Fuel tracking added.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents (overwrites changed files).
3. Commit. Railway redeploys automatically.

## New

### Brokers  (/app/brokers/)
- Add brokers (name, MC #, phone). On any load, pick the **Broker**.
- The Brokers page shows, per company, **how many brokers** you run with, plus a
  table of brokers by load volume, revenue, and which companies they serve.

### Fuel + CSV import  (/app/fuel/ , /app/fuel/import/)
- Import a CSV export from your fuel-card portal (WEX, Comdata, EFS, etc.).
- The importer auto-detects columns (date, amount, gallons, location, card,
  unit) regardless of exact header names, strips $ and commas, and links a
  transaction to a vehicle when the unit number matches.
- Fuel page shows total spend, gallons, and every transaction.

## Integrations still pending credentials
- **TRCeLog ELD (live tracking):** send TRCeLog's API docs + an API token, or we
  can use an ELD aggregator (e.g. TruckerCloud). Then we wire live GPS/HOS.
- **WEX API (auto fuel sync):** send your WEX API token and we switch fuel from
  CSV upload to automatic sync.
- **Highway:** needs a partner/API agreement with Highway; the Brokers feature
  covers "brokers per company" natively in the meantime.

# Trucking Compliance Services — Operations Portal (COMPLETE)

Import loads from CSV / spreadsheet (Amazon Relay & any TMS export).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: Import loads from CSV
Loads page -> "Import loads from CSV" (or /app/loads/import/).
1. Export your loads from Amazon Relay as a CSV/spreadsheet (first row = headers).
2. Upload it. Optionally assign all imported loads to a driver and/or truck.
3. It auto-recognizes columns: Trip/VRID/Load ID, Origin, Destination,
   Pickup date, Delivery date, Rate, Loaded miles, Deadhead miles, Customer.
Loads whose reference already exists are SKIPPED (no duplicates). Unrecognized
columns are ignored. Dates accept 2026-08-10 and 08/10/2026 formats.

Note: this is a manual import (no Amazon login needed). True auto-fetch needs
Amazon Relay API access from Amazon — bring me their API docs if you get them.

## Includes everything to date
CSV load import, hide load $, pay basis, rental contracts, manual load add,
settlement tools, pay history, miles+deadhead, percentage pay, reimbursements.

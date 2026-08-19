# Trucking Compliance Services — Operations Portal (COMPLETE)

Fix: per-truck P&L date filter no longer hides loads (pickup OR delivery date).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What this fixes
On the per-truck P&L report, selecting a date range and clicking Apply appeared
to do "nothing" (empty/zeros). Cause: it filtered loads by PICKUP date only, so
any load without a pickup date dropped out of the range. Now a load counts if its
PICKUP or DELIVERY date falls in the range. Loads with no dates still show when no
range is applied. Applies to both the summary and the single-truck report + PDF.

TIP: for the cleanest reports, set pickup/delivery dates on your loads.

## Includes everything to date
Truck P&L date fix, automated test suite, factoring on add-company, smart doc
viewer, company docs, company logins, FMCSA lookup, multi-stop import, receipts.

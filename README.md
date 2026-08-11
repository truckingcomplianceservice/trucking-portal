# Trucking Compliance Services — Operations Portal

Fix: fuel import auto-detecting the wrong Amount column.

## Deploying this update
1. Unzip and copy ALL contents into your trucking-portal folder (replace all).
2. Commit + push (GitHub Desktop) — Railway redeploys automatically.

## What was wrong
On WEX exports, the importer guessed the **Amount** column as "Invoice" (the
invoice number) instead of "Amt" (the dollars), and "Unit" as "Unit Price".
So the spent amount came in wrong/blank.

## Fixed
Column detection is now priority-based:
- Amount -> the real dollars column (Amt / Amount / Total), never the invoice #.
- Unit -> the truck unit column, never "Unit Price".
- Gallons -> Qty, Date -> Tran Date, Location, Card all detected correctly.
You can still override any column on the confirm screen before importing.

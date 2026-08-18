# Trucking Compliance Services — Operations Portal (COMPLETE)

Five fixes: multi-stop/LTL import, wider rate detection, fuel receipts,
accounting expense receipts, and truck documents (was a deploy/cache issue).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. TEST IN A PRIVATE / INCOGNITO WINDOW first (your normal browser caches old pages).

## What changed
1. LTL / multi-stop loads: the CSV importer now reads every "Stop"/"Location"
   column and stores them all in one load. The load page shows an "All stops" list.
   Origin/Destination auto-fill from the first/last stop when not given separately.
2. Amazon rate: rate detection widened (Block Pay, Line haul, Total pay, Gross pay,
   Charge, etc.) and fixed a bug where "Stop" columns were mistaken for the route.
   If your rate still doesn't import, send the CSV's top header row and I'll tune it.
3. Truck documents: the Documents section is on the truck page (Vehicles -> a truck).
   It was missing only because the older build was still cached/live -- this deploy
   plus an incognito check fixes it.
4. Fuel: "+ Add fuel entry" on the Fuel page lets you add a fuel transaction AND
   attach a receipt/invoice. Existing rows show a receipt "View" or "Attach" link.
5. Accounting: "+ Add expense" lets you add an expense with a receipt. Each expense
   row now has receipt View/Attach and a Remove button.

## Includes everything to date
Multi-stop import, fuel + expense receipts, load docs, truck docs, custom category,
hide load $, pay basis, rental contracts, settlement tools, pay history.

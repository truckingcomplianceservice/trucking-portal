# Trucking Compliance Services — Operations Portal (COMPLETE)

Vehicle documents: view in a popup on the same page (no leaving the page).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## What changed on the truck Documents section
- All documents stay listed on the truck's page.
- Clicking "View" now opens the document in a POPUP VIEWER over the same page
  (PDF/image shows in the popup). Close it (X, Close, or Esc) and you're right
  back on the truck page with the full list.
- There's also "Open in new tab" inside the popup if you want the full window.
- Add (upload) and Remove (delete) stay right there on the page as before.

Includes the earlier fix so a document with no file never crashes the page.

## Includes everything to date
Doc popup viewer, vehicle docs fix, custom category, CSV load import, hide load $,
pay basis, rental contracts, settlement tools, pay history, miles+deadhead.

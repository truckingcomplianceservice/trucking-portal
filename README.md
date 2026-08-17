# Trucking Compliance Services — Operations Portal (COMPLETE)

Fix: vehicle page no longer 500s if a document has no file.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## What this fixes
The truck page crashed (500) whenever a document row had no file attached
(e.g. a partial/failed upload). Now it shows "no file" instead of crashing, so
the page always loads. Uploading real documents works normally.

## Includes everything to date
Vehicle docs fix, custom category, CSV load import, hide load $, pay basis,
rental contracts, settlement tools, pay history, miles+deadhead, percentage pay.

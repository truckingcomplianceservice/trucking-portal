# Trucking Compliance Services — Operations Portal (COMPLETE)

Vehicle documents: custom categories + upload no longer 500s.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## Fixes / additions on vehicle documents
- Upload is now robust: if a file can't be saved it shows a clear message
  instead of a blank 500 error page.
- CUSTOM CATEGORY: pick a Type, or use the new "Or type your own category" box
  (e.g. Cab card, IRP, lease addendum). Whatever you type shows as the document's
  label. Also ensures the upload folder exists on the server volume.

## Includes everything to date
Vehicle documents (+custom category), CSV load import, hide load $, pay basis,
rental contracts, settlement tools, pay history, miles+deadhead, percentage pay.

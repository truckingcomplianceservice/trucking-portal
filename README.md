# Trucking Compliance Services — Operations Portal (COMPLETE)

Documents per vehicle, with expiry tracking + reminders.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: documents on each vehicle
Vehicles -> click a truck -> "Documents" section.
- Upload a file (registration, insurance, inspection, lease, permit, IFTA, title,
  other), give it a title, and an OPTIONAL expiry date.
- Anyone with vehicle access sees the list and can View each document.
- Documents WITH an expiry date show an expiry chip (green/amber/red) and appear
  in your dashboard "expiring soon" reminders -- so you know what's about to lapse.
- Delete removes a document.

Also editable in Admin -> Vehicles (inline) or Admin -> Vehicle documents.

Note: uploaded files live on the Railway volume. Set up file backups (S3/R2)
before relying on this for critical compliance docs.

## Includes everything to date
Vehicle documents, CSV load import, hide load $, pay basis, rental contracts,
manual load add, settlement tools, pay history, miles+deadhead, percentage pay.

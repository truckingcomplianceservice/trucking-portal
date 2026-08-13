# Trucking Compliance Services — Operations Portal (COMPLETE)

Settlement: delete option + delivered-in-week loads auto-attach.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## Fixes
- DELETE a settlement: open the settlement -> "Delete" button (top right).
  It removes the settlement and frees its loads to use again. Asks to confirm.
- Loads now auto-attach if picked up OR delivered within the settlement week
  (so a load delivered that week but picked up earlier is now included).

## If a load still doesn't appear
A load only attaches if its DRIVER is set to that driver. To include any load
manually: open the settlement -> "Loads covered" -> "+ Add a load" dropdown
(shows that driver's loads not already on a settlement). If the load isn't in
the dropdown, its Driver field isn't set to that driver — set it on the load.

## Includes everything to date
Delete/auto-attach fixes, pay history, miles+deadhead, address/phone letterhead,
percentage pay, reimbursements, per-truck & per-driver detail, team comms.

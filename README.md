# Trucking Compliance Services — Operations Portal (COMPLETE)

Add a load MANUALLY on a settlement (for loads not in the system yet).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: add a load manually on the settlement
On a settlement, under "Loads covered", there's now:
"+ Add a load manually (not in the system yet)"
Click it, fill in ref #, pickup date, from/to, loaded + deadhead miles, and rate,
then "Add this load". It creates the load, assigns it to this driver, and attaches
it to the settlement in one step. It shows on the statement like any other load.

Note: a manually-added load becomes a real load record for this driver (so it
stays consistent with reports). Use the normal Loads screen if you also need BOL/POD.

## Includes everything to date
Manual load add, add-load 500 fix, settlement delete + auto-attach, pay history,
miles+deadhead, address/phone, percentage pay, reimbursements, per-truck/driver detail.

# Trucking Compliance Services — Operations Portal (COMPLETE)

Driver pay: percentage-of-load pay + a direct reimbursement box.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New on driver settlements

### Percentage of load
Set a driver's pay type to "Percentage of load" and a rate (e.g. 25) on the
driver's record. New settlements then auto-suggest gross = that % of the loads.
On any settlement you can also type a % in "Set gross as % of loads" and click
Apply % to recalculate on the spot.

### Reimburse money to the driver
The settlement now has an "Extra reimbursement to driver" box (in Edit amounts).
Type any amount you owe the driver back and it's added to net pay. This is
separate from out-of-pocket expense reimbursements (those still add automatically).
Net pay = gross - deductions + out-of-pocket + extra reimbursement.
Both show on the driver's PDF/emailed statement.

## Includes everything to date
Percentage pay + reimbursement, settlement loads breakdown, driver pay,
per-truck & per-driver detail, team communication, tasks + performance, portals.

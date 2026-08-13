# Trucking Compliance Services — Operations Portal (COMPLETE)

Settlement sheet: miles + deadhead, company address & phone.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## What changed on the driver settlement sheet
- Company NAME, ADDRESS, PHONE (+ MC/DOT/CA, email) at the top (letterhead).
  -> Fill these in: Admin -> Companies -> Address / Phone.
- Loads table now shows LOADED miles, DEADHEAD (empty) miles, and TOTAL miles
  per load, plus grand totals, alongside From/To and rate.

## Entering deadhead miles
New field on each load: Admin -> Loads -> a load -> "Deadhead (empty) miles".
Loaded miles is the existing "miles" field. Total = loaded + deadhead.

## Includes everything to date
Settlement miles+deadhead+address+phone, routes, percentage pay + reimbursement,
settlement loads, driver pay, per-truck & per-driver detail, team comms, portals.

# Trucking Compliance Services — Operations Portal (COMPLETE)

Manual Add Load with MULTIPLE STOPS (LTL) + miles total incl. deadhead.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: proper Add Load page (Dispatch -> Loads -> "+ New load")
- Add MULTIPLE STOPS in order (Pickup, Stop 2, Stop 3 ... Delivery). Click
  "+ Add another stop" for LTL / multi-stop trips. First stop = pickup,
  last = final delivery. All stops are saved and shown on the load.
- Miles: enter Loaded miles + Deadhead miles; "Total miles" adds them live
  (total includes deadhead).
- Rate, dates, driver, truck as usual.
No more going into the technical Admin to add a load.

## About Amazon CSV import
The importer reads "Stop"/"Location" columns if your Amazon file has them. If
your export names columns differently and stops still don't import, send me the
top header row of the CSV and I'll match your exact columns.

## Includes everything to date
Manual multi-stop load, truck P&L date fix, test suite, factoring, doc viewer,
company docs, company logins, FMCSA lookup, receipts.

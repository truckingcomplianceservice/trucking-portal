# Trucking Compliance Services — Operations Portal (COMPLETE)

Driver settlement PDF: company address + clear From/To route per load.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## What changed on the driver settlement sheet
- FIX: the downloadable PDF now includes the loads (before, only the emailed one did).
- Company NAME + ADDRESS (+ MC/DOT/CA, phone, email) show at the top via letterhead.
  -> Make sure each company's Address is filled in: Admin -> Companies -> Address.
- "Loads covered (what this pay is for)" table now has clear FROM and TO columns
  so the driver sees exactly which loads, from where to where, they're paid for.

## Includes everything to date
Settlement sheet with address + routes, percentage pay + reimbursement,
settlement loads, driver pay, per-truck & per-driver detail, team comms, portals.

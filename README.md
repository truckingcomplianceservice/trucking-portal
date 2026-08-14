# Trucking Compliance Services — Operations Portal (COMPLETE)

Per-settlement: hide load $ amounts (driver sees route + pay, not load rate).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: hide load amounts (per settlement)
On any settlement, "Loads covered" has a "Hide $ amounts" / "Show $ amounts"
button. When hidden:
- The per-load RATE column disappears on screen AND on the PDF/email statement.
- The driver still sees the ROUTES, MILES, and their GROSS/NET pay -- just not
  what each load paid. Click again to show amounts. It's per settlement.

## Pay type (Weekly / Daily / Per load) — how to use
Driver pay -> New settlement -> "Pay type" dropdown:
- Weekly: pick a week.  - Daily: pick one day.  - Per load: starts empty, you add
the exact loads. Each settlement is labeled with its type. (If you don't see the
Pay type dropdown, hard-refresh the New settlement page after deploying.)

## Includes everything to date
Hide load $ + pay basis, rental contracts, manual load add, settlement tools,
pay history, miles+deadhead, address/phone, percentage pay, reimbursements.

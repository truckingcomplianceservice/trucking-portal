# Trucking Compliance Services — Operations Portal (COMPLETE)

Driver pay: choose Weekly / Daily / Per load; each settlement is labeled.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: pick how you pay when creating a settlement
Driver pay -> New settlement -> "Pay type":
- Weekly  : pick a week; pulls that week's loads (as before).
- Daily   : pick ONE day; pulls that day's loads. Great for daily pay.
- Per load / round trip : starts EMPTY; you add the exact loads/trips you're
  paying for (dropdown or "+ Add a load manually"). Great for per-trip pay.

Each settlement is LABELED (Daily / Weekly / Per load) on the list and on the
settlement page, so you can see how each one was paid. A load never gets paid
twice (once it's on a settlement it won't auto-pull into another).

## Includes everything to date
Weekly/Daily/Per-load pay, rental contracts + P&L, manual load add, settlement
tools, pay history, miles+deadhead, address/phone, percentage pay, reimbursements.

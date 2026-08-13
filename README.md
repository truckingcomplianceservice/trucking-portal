# Trucking Compliance Services — Operations Portal (COMPLETE)

Driver pay history (month / year / all-time) + miles & deadhead on statement.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New: "Paid to date" for each driver
On a driver's settlement page AND on their full report, you now see:
- This month paid, This year paid, All-time paid (counts PAID settlements only)
- A per-month breakdown for the current year
Totals use each settlement's net pay and its paid date.

## About company address/phone on the statement
The statement DOES print company address + phone — but only if those fields are
filled in. If you only see the name, fill them in:
Admin -> Companies -> your company -> Address + Phone -> Save. Then re-open the PDF.

## Also on the statement (from prior build)
Loaded miles, deadhead miles, total miles per load + grand totals; From/To route.

## Includes everything to date
Pay history, miles+deadhead, address/phone letterhead, percentage pay,
reimbursements, settlement loads, per-truck & per-driver detail, team comms.

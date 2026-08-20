# Trucking Compliance Services — Operations Portal

IFTA quarterly fuel-tax worksheet (administrators only).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: IFTA (sidebar -> "IFTA", admin/owner only)
Calculates your quarterly IFTA fuel tax by state.

HOW IT WORKS:
- Pick a quarter + year.
- GALLONS PURCHASED per state are pulled AUTOMATICALLY from your fuel records
  (so set the State on each fuel entry -- there's now a "State (IFTA)" box on the
  Fuel page, and a column in Admin -> Fuel transactions you can edit in bulk).
- YOU ENTER: miles driven in each state, and each state's tax rate for that
  quarter (rates change quarterly -- get them from your IFTA packet / base state
  rate sheet; I can't look them up).
- It computes: fleet MPG (total miles / total gallons), taxable gallons per state
  (miles / MPG), net gallons (taxable - purchased), and tax owed or credit per
  state, plus the net total.
- Saves your entries per quarter so you don't re-type them.

IMPORTANT HONESTY:
- This is a WORKSHEET to help you file (or hand to your accountant). It is NOT an
  official return and does NOT submit to any state.
- Accuracy depends on your data: every fuel purchase needs its state + gallons,
  and you must enter miles per state. Verify before filing.
- Miles-per-state is entered by hand for now (your loads store total miles, not
  per-state miles). A future upgrade with Google routing could estimate the
  state-by-state split automatically.

## Includes everything to date
IFTA worksheet, company switcher fix, deadhead nearby-city fix + auto-fill, chat
+ task files, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

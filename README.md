# Trucking Compliance Services — Operations Portal (COMPLETE)

Settlements now show WHICH LOADS the pay covers (auto + you can override).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> type Summary -> Commit to main -> Push origin.
3. Hard-refresh (Cmd+Shift+R).

## New on driver settlements
When you create a weekly settlement, it AUTOMATICALLY attaches the driver's loads
delivered/picked up in that week, and suggests the gross from their rates.
On the settlement you can then:
- See the "Loads covered" list (ref, route, rate) with a total
- Remove any load, or Add another load (dropdown of his other loads)
- Click "Use loads total as gross" to set pay from the loads, OR type your own gross
The driver's PDF/emailed statement now lists exactly which loads the pay is for.

Auto by default, fully editable by you or your team — you decide the final pay.

## Includes everything to date
Settlement loads breakdown, driver pay, per-truck & per-driver detail, team
communication, tasks + performance, branded portals, role-based access, email.

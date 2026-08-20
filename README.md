# Trucking Compliance Services — Operations Portal

Vehicle cost breakdown by category, with percentages.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: cost breakdown by category (%)
On each truck's Vehicle page, there's now a "Cost breakdown by category" section
showing what share each cost type is of the truck's total spend -- with a
percentage and a bar for each. Example: Fuel 50%, Service/maintenance 20%,
Tires 20%, Wages 10%.

It combines all cost sources for that truck:
- Fuel (from fuel transactions)
- Service / maintenance (from service records)
- Every expense category you logged in Accounting (Tires, Wages, Insurance, etc.)

Percentages are each category's share of the truck's grand total, sorted biggest
first. This makes it easy to see where the money goes on each vehicle.

## Includes everything to date
Vehicle cost % breakdown, vehicle-expense display fix, IFTA worksheet, company
switcher fix, deadhead nearby-city fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

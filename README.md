# Trucking Compliance Services — Operations Portal

Brokers as proper records: dropdown on every load, add-new from the rate con,
and per-agent contacts (name + phone + extension, e.g. each TQL rep).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: brokers + agents
On the Add Load page:
- "Broker" is now a DROPDOWN of your saved brokers (not free text).
- Pick "+ Add a new broker..." to add one right there from the rate confirmation:
  company name, MC number, main phone, email, address, city, state -- and
  optionally the agent you booked with (name + direct phone + extension).
- When you pick an existing broker, an "Agent / rep" dropdown shows that broker's
  agents (with phone + extension) so you can select the exact person -- e.g. for
  TQL, choose the specific rep you worked with.

Broker fields added: address, city, state, ZIP (plus existing MC, phone, email).
New "Broker agents" list: each agent belongs to a broker and has their own phone
and extension. The load records both the broker AND the specific agent.

Manage brokers/agents anytime in Admin -> Brokers (agents show as an inline list
under each broker), or add them on the fly from the load form.

## Includes everything to date
Brokers + agents, team messages, admin-only delete, vehicle page fix, deadhead
fix + Google-ready miles, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, professional
1099, R2 cloud backup, 12-test suite, factoring, company docs, company logins,
FMCSA lookup.

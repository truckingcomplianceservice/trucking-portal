# Trucking Compliance Services — Operations Portal

Rate-con auto-fill now also creates the broker (with contact info) AND the agent.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What's new
When you create a load from a rate confirmation (with the AI key set), it now
extracts and AUTO-CREATES:
- The BROKER as a full record: name, MC number, phone, email, address, city,
  state -- and it shows in your Brokers list immediately.
- The AGENT / rep who booked it: name, direct phone, and extension (e.g. your
  TQL rep) -- saved under that broker.
- The load is linked to BOTH the broker and that specific agent.

Smart matching: if the broker already exists (by MC number or name), it reuses it
instead of creating a duplicate -- and fills in any missing contact details. Same
for the agent (no duplicate reps).

Still review the draft before final save -- AI extraction is very good but not
perfect, so glance at the rate and broker before confirming.

## Includes everything to date
Rate-con broker+agent auto-create, all-brokers list, brokers + agents, team
messages, admin-only delete, vehicle page fix, deadhead fix + Google-ready miles,
unified load form, vehicle docs front, auto miles, vehicle photos, email document,
hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup, 12-test
suite, factoring, company docs, company logins, FMCSA lookup.

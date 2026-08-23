# Trucking Compliance Services — Operations Portal

Broker detail page: click a broker to see everything about them.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Broker detail page
On the Brokers page, CLICK ANY BROKER to open their full detail page. It shows:

- BROKER DETAILS: MC number, phone, email, address, notes (Edit link to change).
- BUSINESS SUMMARY: how many loads you've done with them, total revenue, and how
  much is paid/released.
- AGENTS: every agent for this broker, each with their phone, email, and how many
  loads + revenue came through that agent.
  * ADD an agent with the "+ Add agent" button (managers/admins).
  * REMOVE an agent with the Remove button (admins only).
- LOADS WITH THIS BROKER: every load you ran with them -- pickup date, reference,
  route, driver, agent, status, and rate -- with a total at the bottom.
  * FILTER BY DATE: pick a From/To date range to see loads done in a specific
    period (e.g. "what did we do with this broker in August").
  * Click any load row to open that load's full detail.

Now you can manage a broker relationship end to end from one page.

## Includes everything to date
Broker detail page (agents + load history + date filter), driver wages detail,
wages on single-truck report, reports label fix, per-truck driver-wage
attribution, team invite + approval, per-truck P&L expense fix, improved rate-con
broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA worksheet,
company switcher fix, deadhead nearby-city fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

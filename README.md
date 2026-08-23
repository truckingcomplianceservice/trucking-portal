# Trucking Compliance Services — Operations Portal

Driver invite links: two ways for drivers to self-register for the portal.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Driver invite links (both options you asked for)

OPTION A -- Link tied to an EXISTING driver:
  Drivers -> click a driver -> "Driver portal login" card ->
  "Create invite link for this driver". Send the link; they set their own
  password; you approve; it links to THAT driver record.

OPTION B -- General driver link (they fill in their own details):
  Drivers page -> "Invite driver by link" button. Send the link; the person
  fills in their name + password; you approve; a NEW driver record is created
  and linked automatically.

WHERE TO FIND / APPROVE:
- Open invite links show on the Drivers page ("Open driver invite links").
- When a driver signs up, they appear under "Drivers awaiting approval" on the
  Drivers page with Approve / Reject buttons. They cannot log in until approved.

You now have BOTH ways to onboard a driver:
- Instant: the "Create driver login" button (you set username + password).
- Self-serve: invite links (they set their own password, you approve).

SECURITY: same as team invites -- long unguessable token, expires in 7 days,
account inactive until you approve, driver is not staff and sees only their own
data.

## Includes everything to date
Driver invite links, create-driver-login button, driver portal, IFTA print,
broker detail page, driver wages detail, wages on single-truck report, per-truck
driver-wage attribution, team invite + approval, per-truck P&L expense fix,
improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead fix + auto-fill, chat + task files,
notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, admin-only
delete, vehicle page fix, unified load form, vehicle docs front, auto miles,
vehicle photos, email document, hiring phases 1-6, dashboard KPIs, 1099, R2 cloud
backup, 12-test suite, factoring, company docs, company logins, FMCSA lookup.

# Trucking Compliance Services — Operations Portal

Floating team chat (bottom-right) + pinned shift-handoff note. Company-private.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: floating team chat + shift handoff
- A "Team chat" button sits in the BOTTOM-RIGHT corner of every page. Click it to
  open a chat panel; click the X to shrink it back to a button.
- Everyone in the SAME company can chat together in real-ish time (the panel
  refreshes every ~4 seconds, so messages appear within a few seconds). Messages
  never cross between companies.
- Pinned SHIFT HANDOFF note at the top of the panel: the person going off shift
  writes what's happening (active loads, what brokers/drivers are waiting for),
  clicks Save, and the next person sees it immediately -- so they can respond to
  brokers and drivers professionally without missing context.

Available to every team member of a company. Owner sees the active company's chat.

HONEST NOTE: this refreshes every few seconds (not truly instant like WhatsApp).
True instant messaging needs more complex live-connection tech; this polling
approach is reliable and feels close. No mobile push notifications.

## Includes everything to date
Floating team chat + handoff, duplicate rate-con protection, rate-con broker+agent
auto-create, all-brokers list, brokers + agents, team messages, admin-only delete,
vehicle page fix, deadhead fix + Google-ready miles, unified load form, vehicle
docs front, auto miles, vehicle photos, email document, hiring phases 1-6,
dashboard KPIs, professional 1099, R2 cloud backup, 12-test suite, factoring,
company docs, company logins, FMCSA lookup.

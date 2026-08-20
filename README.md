# Trucking Compliance Services — Operations Portal

Invite team members by link -> they self-register -> you approve them.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: invite by link + self sign-up + approval
On the Team page (managers/admins only), there's now a "Invite by link" button.

HOW IT WORKS:
1. Click "Invite by link", pick the ROLE for the new person (and optionally their
   email), and create the invite. You get a secure link (expires in 7 days).
2. Send that link to the person (text, email, WhatsApp -- however you like).
3. They open it, fill in their name + username + EMAIL, and SET THEIR OWN PASSWORD.
   They can't pick "admin" -- only the role you assigned.
4. They land in an "awaiting approval" state -- they CANNOT log in yet.
5. You (and your managers) get a notification. On the Team page you'll see
   "Awaiting your approval" with Approve / Reject buttons.
6. When you Approve, their account activates and they can log in -- seeing only
   what their role allows, for your company only.

SECURITY (built in):
- The link uses a long, unguessable token and expires in 7 days.
- New accounts are created INACTIVE and cannot log in until you approve them.
- Only managers/admins can create invites or approve; only admins can invite
  another admin.
- The person is tied to YOUR company only -- full data isolation preserved.

Roles already control what each member can see/do (admin, manager, dispatcher,
compliance, safety, accountant, billing, driver) -- this just lets people join
themselves and set their own password, with your approval.

## Includes everything to date
Invite-by-link + self-signup + approval, per-truck P&L expense fix, improved
rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix, IFTA
worksheet, company switcher fix, deadhead nearby-city fix + auto-fill, chat +
task files, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

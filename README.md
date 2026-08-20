# Trucking Compliance Services — Operations Portal

Notification system: in-app bell + email. Assignees can respond to tasks.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: notifications (bell + email)
- A NOTIFICATION BELL now sits in the top bar (top-right) on every page, with a
  red unread count. Click it to see recent notifications; "Mark all read" clears
  them. It refreshes every 20 seconds.
- People get notified (in-app AND by email) when:
  * a task is ASSIGNED to them,
  * someone RESPONDS to their task,
  * a task they created is marked DONE,
  * someone @MENTIONS them in team chat.

## New: respond to tasks
On the Tasks page, each task now has a "Respond" link. Click it to see the
conversation and post a response. When you respond, the task's creator (and
assignee) get notified -- so you can assign a task, the person can reply, and
you'll know. Great for back-and-forth without leaving the app.

## Email note
Notification emails use your existing company email setup. Make sure each team
member has an EMAIL set on their account (Team -> Edit) to receive emails; the
in-app bell works regardless.

SMS/phone text is NOT included yet (that needs a paid Twilio account + business
registration) -- we can add it later as an upgrade.

## Includes everything to date
Notifications (bell+email) + task responses, chat @mentions + chat-to-task, team
username + remove, floating team chat + handoff, duplicate rate-con protection,
rate-con broker+agent auto-create, all-brokers list, brokers + agents, team
messages, admin-only delete, vehicle page fix, deadhead fix + Google-ready miles,
unified load form, vehicle docs front, auto miles, vehicle photos, email document,
hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud backup, 12-test
suite, factoring, company docs, company logins, FMCSA lookup.

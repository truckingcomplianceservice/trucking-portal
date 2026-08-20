# Trucking Compliance Services — Operations Portal

Team chat: @mention tagging + turn a message into an assigned task.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New in the team chat widget
- @MENTION / TAGGING: type "@" in the chat and a list of your teammates pops up.
  Pick one to tag them (e.g. "@alice call TQL"). Tagged people see that message
  highlighted (a gold outline) so they know it's for them. Mentions are shown in
  gold in the text.
- TURN A MESSAGE INTO A TASK: click the "Task" button in the chat. It pre-fills
  the task from what you typed, lets you pick who to assign it to and a priority,
  and creates a real task on the Tasks page. A short confirmation is posted back
  in chat so the team sees it was actioned.

Reminder: full task management already lives on the Tasks page (sidebar "Tasks")
-- assign, set priority/due date, link to a load/driver/truck, mark done. This
just makes it quick to create one straight from a chat message.

All company-private: you can only tag/assign teammates in your own company.

## Includes everything to date
Chat @mentions + chat-to-task, team username + remove, floating team chat +
handoff, duplicate rate-con protection, rate-con broker+agent auto-create,
all-brokers list, brokers + agents, team messages, admin-only delete, vehicle
page fix, deadhead fix + Google-ready miles, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, professional 1099, R2 cloud backup, 12-test suite, factoring, company docs,
company logins, FMCSA lookup.

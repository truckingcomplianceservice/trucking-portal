# Trucking Compliance Services — Operations Portal

Better broker auto-add from rate cons + clear feedback about what happened.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What changed
The broker auto-add from rate cons already existed, but it only worked if the
broker NAME was actually read from the PDF. Two improvements:

1. BETTER BROKER DETECTION without the AI key: the app now looks for a "Broker:"
   (or Brokerage/3PL/Bill To) label and for company-name keywords (logistics,
   transport, freight, etc.), instead of just grabbing the first line. So it finds
   the real broker on many more rate cons.
2. CLEAR FEEDBACK: after upload, you now get a message that says either
   "Broker 'X' was added/linked in your Brokers list (with agent Y)" OR
   "no broker name could be read from this rate confirmation, so none was added --
   set it on the load." No more guessing whether it worked.

IMPORTANT HONESTY: the most reliable extraction still comes from the AI key
(ANTHROPIC_API_KEY in Railway). Without it, the app guesses from text patterns --
much better now, but some rate-con layouts still won't extract the broker cleanly.
If the message says no broker was read, just pick/add the broker on the load; and
consider turning on the AI key for best results.

## Includes everything to date
Improved rate-con broker auto-add, vehicle cost % breakdown, vehicle-expense fix,
IFTA worksheet, company switcher fix, deadhead nearby-city fix + auto-fill, chat +
task files, notifications (bell+email) + task responses, chat @mentions +
chat-to-task, team username + remove, floating team chat + handoff, duplicate
rate-con protection, rate-con broker+agent auto-create, all-brokers list, brokers
+ agents, admin-only delete, vehicle page fix, unified load form, vehicle docs
front, auto miles, vehicle photos, email document, hiring phases 1-6, dashboard
KPIs, 1099, R2 cloud backup, 12-test suite, factoring, company docs, company
logins, FMCSA lookup.

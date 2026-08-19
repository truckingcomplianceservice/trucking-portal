# Trucking Compliance Services — Operations Portal

Vehicle documents front-and-center (+ fixes a doc-name display bug).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## Vehicle documents
- The Vehicles list now shows a "Docs" column: how many documents (and photos)
  each truck has, at a glance.
- Click any unit -> its page shows all documents with View, Email, Delete, and
  an Upload form to add more (registration, insurance, inspection, lease, permits,
  IFTA, cab card, or your own category + expiry date).
- NEW: "Email" button on each vehicle document -- send it to anyone from your
  company email (reply-to = your company).
- FIX: vehicle document names/titles now display correctly (a label was not
  showing before).

## Includes everything to date
Vehicle docs front + email + name fix, auto miles estimate, vehicle photos,
email document, hiring phases 1-6, dashboard KPIs, professional 1099, R2 cloud
backup, multi-stop load, truck P&L date fix, 12-test suite, factoring, doc
viewer, company docs, company logins, FMCSA lookup.

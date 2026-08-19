# Trucking Compliance Services — Operations Portal (COMPLETE)

Factoring dropdown now on the in-app Add Company page.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## What changed
When you add a company (All companies -> "+ Add company"), there's now a
"Factoring company" dropdown with all the well-known factors (RTS, Bobtail,
TAFS, Apex, TBS, OTR, Triumph, eCapital, Riviera, Porter, Compass, England,
Thunder, Phoenix, Single Point, Love's/TFS). Choose "Other" to type any factor.
Pick it right when creating the company -- no need to go into Admin.

## Includes everything to date
Factoring on add-company, factoring list, smart doc viewer, company docs,
company logins, FMCSA lookup, multi-stop import, fuel + expense receipts, docs.

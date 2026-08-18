# Trucking Compliance Services — Operations Portal (COMPLETE)

Company documents: MC letter, COI, IFTA, MCP letter and all operating paperwork.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: Company documents (sidebar -> "Company docs")
A place for company-level paperwork that isn't tied to a specific truck or load:
- MC authority letter, COI (insurance), IFTA, MCP letter, W-9, Notice of
  Assignment, UCR, BOC-3, EIN letter, operating authority -- or your own category.
- Upload with an optional expiry date; expiring items show a color chip AND
  appear in the dashboard reminders.
- "View" opens the document in a POPUP over the page (Esc/Close to return).
- Delete removes a document.

Scoped per company: each company login sees ONLY their own paperwork. As owner,
use the top-right switcher to view any company's documents (or upload for them).

## Three document homes now
- Company docs (MC/COI/IFTA/MCP...) -> sidebar "Company docs"
- Truck docs (registration/insurance/inspection) -> a truck's page
- Load docs (POD/Rate con/BOL) -> a load's page

## Reminder: file backups still pending (do before paying customers).

## Includes everything to date
Company docs, company logins, FMCSA lookup, multi-stop import, fuel + expense
receipts, load docs, truck docs, hide load $, pay basis, rental contracts.

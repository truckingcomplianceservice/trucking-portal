# Trucking Compliance Services — Operations Portal (COMPLETE)

Stage 1 multi-company: create a separate login per company (their own data + logo).

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: give a company its own login
All companies -> "Company logins":
- Pick the company, set a username + password, choose access level, Create login.
- That login is tied to ONE company. They sign in at /c/<their-slug>/ and see ONLY
  their own dashboard, trucks, loads, accounting, expenses, and documents -- with
  their own logo. They cannot see any other company's data (tested and enforced,
  including direct-URL attempts).
- Share their sign-in link + username/password with them.

## Notes for selling to outside companies (important)
- FILE BACKUPS are still not set up. The database is backed up daily, but uploaded
  files (documents, receipts, PODs, logos) are NOT. Set up file backup (S3/R2)
  BEFORE onboarding paying customers -- this is the top priority.
- Legal: Terms of Service + Privacy Policy needed once you hold other companies'
  data (a lawyer conversation).
- This is Stage 1 (you create logins). Self-serve signup and billing are later stages.

## Includes everything to date
Company logins, FMCSA lookup, multi-stop import, fuel + expense receipts, load docs,
truck docs, custom category, hide load $, pay basis, rental contracts, pay history.

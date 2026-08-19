# Trucking Compliance Services — Operations Portal (COMPLETE)

Professional 1099-NEC with all fields + completeness check.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## Improved 1099-NEC (Tax & 1099s -> a 1099 driver -> generate)
- Clean, professional 1099-NEC layout (Copy B, official box structure).
- All fields filled from your records: Payer name/DBA/address/phone/EIN/state no.,
  Recipient name/address/TIN, Box 1 nonemployee compensation, account number.
- Box 1 = total of that driver's PAID settlements in the tax year.
- COMPLETENESS CHECK: if anything required is missing, the form shows a red
  "Incomplete" banner listing exactly what to add (and where). If all good, it
  shows a green "Complete" banner. Missing fields print [MISSING] in red instead
  of a silent blank -- so you never file an incomplete form by accident.

## To fill everything in
- Payer (company): Admin -> Companies -> EIN, address, phone, and new fields
  "DBA name", "State (2-letter)", "State tax / payer state no.".
- Recipient (driver): Admin -> Drivers -> tax status = 1099, Tax ID (SSN/EIN),
  address.
- Pay: mark the driver's settlements PAID with a paid date in the tax year.

Note: this is a data summary for your convenience -- file on the official IRS
form or via an authorized e-file provider. Not tax advice.

## Includes everything to date
Professional 1099, R2 cloud backup, multi-stop load, truck P&L date fix, test
suite, factoring, doc viewer, company docs, company logins, FMCSA lookup.

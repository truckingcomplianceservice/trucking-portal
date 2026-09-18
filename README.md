# Trucking Compliance Services — Operations Portal

Search settlements by driver or company + see totals paid/unpaid.

## Deploy
1. Download this zip, then in Terminal:
   cd ~/Documents/GitHub/trucking-portal && rm -rf operations trucking_ops templates manage.py requirements.txt Procfile README.md && unzip -o ~/Downloads/<THIS-FILE>.zip -d . && echo DONE
2. GitHub Desktop -> Commit -> Push. Test in a private/incognito window.

## New: search on the Driver pay page
On Driver pay there's now a search box: type a DRIVER name (or company name) and:
- The list filters to that driver's/company's settlements only.
- A summary shows: how many settlements, TOTAL PAID, and total unpaid for them.
- Below it, the complete settlement history for that driver/company is listed.

So you can quickly answer "how much have I paid this driver in total, and what's
their full history" -- just type their name and search. Works with the All / Unpaid
/ Paid filters too. Also matches an owner-operator's business (pay-to) name.

Example: search "Harjeet" -> 3 settlements, Total paid $3,500, unpaid $1,800, with
all three periods listed.

## Includes everything to date
Settlement search + totals, check amount nudge, rebrand to Trucking Compliance
Services, self-serve signup + 7-day trial, hide-load-amounts consistency,
owner-operator company pay + EIN on 1099, driver pay-to business name, IFTA CSV
import, P&L partner breakdown, partner statement, expense Paid-by, partner ledger,
loads on check stub, LMP100 check layout, load photos, driver check printing,
invoice load search + auto-fill, P&L miles + $/mi, auto loaded-miles, invoice
unpaid-until-paid, invoice line items + email, searchable load picker, wage
calculator, daily/per-load/percentage settlements, driver-only load picker,
settlement PDF itemized, itemized settlement lines, driver settlement detail,
settlement layout fix, easy driver-wage creation, rental truck swap, photo viewer
fix, truck photo gallery, office PWA + mobile, phone tap-to-call + phone login +
SMS-ready, driver nav + status + scanner, location notice, driver map, driver
tracking, driver PWA, driver load detail, driver login fix, driver invite links,
create-driver-login, driver portal, IFTA print, broker detail, driver wages
detail, per-truck wages, team invite, per-truck P&L fix, rate-con auto-add,
vehicle cost %, vehicle-expense fix, IFTA worksheet, company switcher fix, deadhead
fix, chat + task files, notifications, chat mentions, team tools, rate-con
protection, brokers + agents, admin delete, vehicle fix, unified load form, auto
miles, vehicle photos, email doc, hiring 1-6, dashboard KPIs, 1099, R2 backup,
tests, factoring, company docs, company logins, FMCSA lookup.

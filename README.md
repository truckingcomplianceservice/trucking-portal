# Trucking Compliance Services — Operations Portal (COMPLETE)

Adds role-based access: each user only sees and reaches their own areas.

## Deploy (one upload — this zip has everything)
1. Unzip -> copy ALL contents into your trucking-portal folder -> Replace all.
2. GitHub Desktop -> Commit -> Push -> wait for Railway "Successful".

## How role access works now
Set each person's Role on Team -> Edit. The menu hides what they can't use, and
pages block direct access too (no sneaking in by URL).

- Owner (you): everything. ONLY you can see All Companies (portfolio money),
  delete records, grant the Admin role, and change notification rules.
- Manager: all operations + manage team. Cannot see the all-companies money
  view, cannot delete, cannot make someone an Admin.
- Dispatcher: Dashboard, Dispatch/Loads, Brokers, Drivers, Vehicles.
- Billing: Dashboard, Billing, Accounting, Tax/1099s, Reports.
- Accountant: same as Billing plus Fuel.
- Compliance: Dashboard, Drivers, Vehicles, Hiring, Compliance.
- Safety: Dashboard, Drivers, Vehicles, Compliance.
- Driver: Dashboard only (they use the public upload link).

Company separation still applies on top of this: people only see the companies
you assigned them.

## Includes everything to date
Role-based access, background email (never hangs a save), email 465/SSL support,
load filters, team edit/reset/invite, all fuel fixes + dedup + edit/delete,
expense fix, portfolio, factoring aging, maintenance, DQF, billing + aging.

# Trucking Compliance Services — Operations Portal (COMPLETE)

Adds Tasks (assign work) and Performance (per person + per truck).

## Deploy (one upload — this zip has everything)
1. Unzip -> copy ALL contents into your trucking-portal folder -> Replace all.
2. GitHub Desktop -> Commit -> Push -> wait for Railway "Successful".
(There is a new migration for Tasks + Performance notes — it runs automatically.)

## New: Tasks (sidebar -> Tasks)
- Managers/owner assign tasks to a team member OR a driver, with due date,
  priority, and an optional linked truck/load.
- Each person sees only the tasks assigned to them; managers see all.
- Change status with the dropdown (Open / In progress / Done / Cancelled).
  Overdue due-dates show in red.

## New: Performance (sidebar -> Performance, under Reports)
Auto stats plus your own notes:
- Drivers: loads, revenue, average rating, note count.
- Trucks: loads, revenue, fuel, average rating, note count.
- Team members: tasks assigned / done / open.
- Click "+ note" on any row to add a dated note and an optional 1-5 rating.
- Date-range filter at the top.

Everything is company-scoped and respects roles: Performance sits under the
"reports" permission; Tasks are visible to everyone (but non-managers only see
their own and can only self-assign).

## Includes everything to date
Tasks + performance, branded portal login, role-based access, per-truck P&L,
per-company logos, background email, email 465/SSL, load filters,
team edit/reset/invite, fuel fixes + dedup, expense fix, portfolio, aging.

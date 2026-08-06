# Trucking Compliance Services — Operations Portal

Multi-company TMS with a full team management system, time clock, branded UI,
operations, hiring, compliance, factoring, tax/1099s, brokers, and fuel.

## Deploying this update
1. In your `trucking-portal` repo: **Add file -> Upload files**.
2. Unzip and drag in ALL the contents, including `operations/static/logo.png`.
3. Commit. Railway redeploys automatically.

## New in this update

### Logo fixed
The logo now displays on white (the black-box bug is gone).

### Team management  (sidebar: Team)
- **Roster** of everyone with role, companies, active status, and today's hours.
- **Add team member** (managers only): name, username, temp password, role
  (Dispatcher, Compliance manager, Safety officer, Accountant, Billing, Manager,
  Admin, Driver), and which companies they can access. Creates their login and
  sets role-based permissions automatically.
- **Deactivate / reactivate** members (this is how you "remove" access).

### Time clock
- Each person clocks **in/out** from the Team page.
- Roster shows who's **on the clock** and their **hours today**.
- **Timesheet** page: full check-in / check-out history with hours.

### Who's doing what
- Activity now records **which user** did each action (booked a load, added an
  expense, clocked in, added a team member, etc.), shown on the Team page and the
  full activity feed.

## Role permissions (starting point)
- Dispatcher: loads, drivers, vehicles, brokers
- Compliance / Safety: compliance documents, applicants, drivers, vehicles
- Accountant / Billing: expenses, settlements, fuel
- Manager / Admin: everything
Everyone can view; these can be fine-tuned later.

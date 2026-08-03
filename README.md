# Trucking Operations Portal — Phase 1

The foundation of your system: **Companies** (each with MC / DOT / CA and factor),
**Drivers** (with type and tax status), **Vehicles**, **Loads**, and **logins**
with per-company access. Built with Django, ready to deploy on Railway.

## What Phase 1 does

- **Companies** — name, MC#, DOT#, CA#, and factoring company (RTS / Bobtail / etc.)
- **Drivers** — CDL & medical expiry, company driver vs owner-operator, W-2 vs 1099 tax status, pay type/rate
- **Vehicles** — unit, make/model/year, plate, inspection expiry
- **Loads** — route, rate, miles, status, payment status, assigned driver & vehicle
- **Users & access** — each staff login has a role and a list of companies they can see.
  A person assigned to one company **cannot see another company's** drivers or loads.

You manage everything through Django's built-in admin panel. This is the working
engine; the custom-designed screens from the prototype come in later phases.

## Deploying on Railway (same as before)

1. Upload these files to a GitHub repo (drag the contents: `manage.py`, `Procfile`,
   `requirements.txt`, and the `operations` and `trucking_ops` folders).
2. In Railway: **New Project → GitHub Repo →** pick the repo.
3. Add a **PostgreSQL** database (**+ Add → Database → PostgreSQL**).
4. On the **web** service → **Variables**, add:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `ADMIN_USERNAME` = a username you choose
   - `ADMIN_PASSWORD` = a strong password you choose
   - `ADMIN_EMAIL` = your email
   - `DEBUG` = `False`
5. **Deploy.** When it's Online, open `your-app.up.railway.app/admin/` and log in.

First thing to do after logging in: add your two companies under **Companies**,
then start adding drivers, vehicles, and loads.

## Notes

- **File uploads** (BOL/POD, driver & vehicle documents) come in a later phase,
  once we attach persistent storage — Railway's default storage is temporary,
  so we set that up deliberately when documents arrive.
- **Roles** (who can see what) are enforced by company access now; finer role
  permissions get layered on as accounting, tax, and other modules are built.

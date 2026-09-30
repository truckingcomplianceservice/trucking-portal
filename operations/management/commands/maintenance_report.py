"""Print what the dashboard's maintenance alerts would show, without changing
anything. Read-only: run it against production to preview the alerts and to see
which trucks were skipped for missing data.

    python manage.py maintenance_report
    python manage.py maintenance_report --company 3
"""
from django.core.management.base import BaseCommand

from operations.models import Company, Vehicle
from operations.views import (_maintenance_alerts, _fuel_mileage_alerts,
                              _service_time_alerts, _vehicle_mpg, _service_dates,
                              MPG_MIN_FILLUPS, MPG_MIN_GALLONS, MPG_MIN_MILES,
                              SERVICE_MAX_DAYS)


class Command(BaseCommand):
    help = "Preview the dashboard maintenance alerts (read-only)."

    def add_arguments(self, parser):
        parser.add_argument("--company", type=int, default=None,
                            help="Only this company id (default: every active company).")

    def handle(self, *args, **options):
        companies = Company.objects.all()
        if options["company"]:
            companies = companies.filter(pk=options["company"])
        if not companies:
            self.stdout.write("No companies found.")
            return

        for co in companies:
            vehicles = list(Vehicle.objects.filter(company=co, status="active"))
            self.stdout.write(self.style.MIGRATE_HEADING(
                f"\n{co.name} - {len(vehicles)} active truck(s)"))
            if not vehicles:
                continue
            scope = [co]

            hard = _maintenance_alerts(scope)
            self.stdout.write(f"\n  CONFIRMED overdue/near (odometer): {len(hard)}")
            for a in hard:
                state = (f"OVERDUE by {a['overdue_by']:,} mi" if a["overdue"]
                         else f"{a['miles_to_service']:,} mi left")
                self.stdout.write(f"    Unit {a['unit']}: {state}")

            fuel = _fuel_mileage_alerts(scope)
            self.stdout.write(f"\n  VERIFY MILEAGE (fuel estimate): {len(fuel)}")
            for a in fuel:
                self.stdout.write(
                    f"    Unit {a['unit']}: ~{a['est_miles']:,} mi est since service "
                    f"({a['gallons_since']:,.0f} gal @ {a['mpg']} mpg), "
                    f"odometer reads {a['odometer'] or 'unset'}, "
                    f"{'PAST DUE' if a['est_past_due'] else str(a['est_to_service']) + ' mi to service'}")

            timed = _service_time_alerts(scope)
            self.stdout.write(f"\n  SERVICE CHECK DUE ({SERVICE_MAX_DAYS}+ days): {len(timed)}")
            for a in timed:
                self.stdout.write(f"    Unit {a['unit']}: {a['days']} days since {a['since']}")

            # Why a truck is absent from the fuel check - usually a data gap, not a bug.
            serviced_on = _service_dates(vehicles)
            skipped = []
            for v in vehicles:
                why = []
                if not v.service_interval_miles:
                    why.append("no service_interval_miles")
                if v.last_service_miles is None:
                    why.append("no last_service_miles")
                if v.odometer is None:
                    why.append("no odometer")
                if not serviced_on.get(v.id):
                    why.append("no last service date")
                if not why and _vehicle_mpg(v) is None:
                    why.append(f"not enough fuel/load history for MPG "
                               f"(needs {MPG_MIN_FILLUPS} fill-ups, {MPG_MIN_GALLONS} gal, "
                               f"{MPG_MIN_MILES} mi, and a plausible 3-12 mpg)")
                if why:
                    skipped.append((v.unit_number, "; ".join(why)))
            self.stdout.write(f"\n  SKIPPED for missing data: {len(skipped)}")
            for unit, why in skipped:
                self.stdout.write(f"    Unit {unit}: {why}")

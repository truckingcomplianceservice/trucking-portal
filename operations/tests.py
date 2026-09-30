"""
Automated test suite — checks the whole system's core features.
Run it anytime with:   python manage.py test operations
Each test is one safety check. Green = working, Red = something broke.
"""
import datetime, tempfile
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from operations.models import (Company, Driver, Vehicle, Load, Settlement,
                               Profile, VehicleDocument, CompanyDocument,
                               FuelTransaction, Expense, Applicant)

MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA, ALLOWED_HOSTS=["testserver", "app.pure99inc.com"],
                   STORAGES={
                       "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                       "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
                   })
class CoreSystemTests(TestCase):
    def setUp(self):
        self.a = Company.objects.create(name="West Gate Carrier LLC", slug="westgate")
        self.b = Company.objects.create(name="Roundway Transport LLC", slug="roundway")
        self.owner = User.objects.create_superuser("owner", password="pw12345678")
        Profile.objects.get_or_create(user=self.owner, defaults={"role": "admin"})
        self.oc = Client(); self.oc.force_login(self.owner)

    def _set_company(self, client, company):
        s = client.session
        s["active_company"] = str(company.id) if company else "all"
        s.save()

    def test_settlement_pay_math(self):
        d = Driver.objects.create(company=self.a, first_name="Ash", last_name="Pal")
        Load.objects.create(company=self.a, driver=d, reference="L1", origin="X", destination="Y", rate=1000, pickup_date=datetime.date(2026,8,10))
        Load.objects.create(company=self.a, driver=d, reference="L2", origin="P", destination="Q", rate=1200, pickup_date=datetime.date(2026,8,11))
        self._set_company(self.oc, self.a)
        self.oc.post("/app/pay/new/", {"driver": str(d.id), "pay_basis":"weekly","period_start":"2026-08-10","period_end":"2026-08-16"})
        s = Settlement.objects.latest("id")
        self.assertEqual(s.loads.count(), 2)
        self.assertEqual(float(s.gross_pay), 2200.0)

    def test_no_double_pay(self):
        d = Driver.objects.create(company=self.a, first_name="Ash", last_name="Pal")
        Load.objects.create(company=self.a, driver=d, reference="L1", origin="X", destination="Y", rate=1000, pickup_date=datetime.date(2026,8,10))
        self._set_company(self.oc, self.a)
        self.oc.post("/app/pay/new/", {"driver":str(d.id),"pay_basis":"weekly","period_start":"2026-08-10","period_end":"2026-08-16"})
        self.oc.post("/app/pay/new/", {"driver":str(d.id),"pay_basis":"weekly","period_start":"2026-08-10","period_end":"2026-08-16"})
        self.assertEqual(Settlement.objects.latest("id").loads.count(), 0)

    def test_company_login_sees_only_own_data(self):
        Vehicle.objects.create(company=self.a, unit_number="A-100")
        vb = Vehicle.objects.create(company=self.b, unit_number="B-200")
        Load.objects.create(company=self.a, reference="AAA", origin="X", destination="Y", rate=1)
        Load.objects.create(company=self.b, reference="BBB", origin="P", destination="Q", rate=1)
        self.oc.post("/app/company/access/", {"company":str(self.a.id),"username":"wg","password":"secret12345","role":"admin"})
        wg = User.objects.get(username="wg"); wc = Client(); wc.force_login(wg)
        loads = wc.get("/app/loads/").content.decode()
        self.assertIn("AAA", loads); self.assertNotIn("BBB", loads)
        r = wc.get(f"/app/vehicles/{vb.id}/")
        self.assertNotIn("B-200", r.content.decode())

    def test_vehicle_document_upload_and_no_crash_when_fileless(self):
        v = Vehicle.objects.create(company=self.a, unit_number="A-1")
        self._set_company(self.oc, self.a)
        f = SimpleUploadedFile("i.pdf", b"%PDF-1.4", content_type="application/pdf")
        self.oc.post(f"/app/vehicles/{v.id}/doc/", {"doc_type":"insurance","title":"COI","file":f})
        self.assertEqual(VehicleDocument.objects.filter(vehicle=v).count(), 1)
        VehicleDocument.objects.create(company=self.a, vehicle=v, doc_type="other", custom_type="nofile")
        self.assertEqual(self.oc.get(f"/app/vehicles/{v.id}/").status_code, 200)

    def test_company_document_upload(self):
        self._set_company(self.oc, self.a)
        f = SimpleUploadedFile("mc.pdf", b"%PDF-1.4", content_type="application/pdf")
        self.oc.post("/app/company/documents/", {"doc_type":"mc_authority","title":"MC Authority","file":f})
        self.assertEqual(CompanyDocument.objects.filter(company=self.a).count(), 1)

    def test_csv_load_import_multistop_and_rate(self):
        self._set_company(self.oc, self.a)
        data = (b"Trip ID,Stop 1,Stop 2,Stop 3,Block Pay,Loaded Miles\n"
                b"T-900,Sacramento CA,Reno NV,Las Vegas NV,1875.50,560\n")
        f = SimpleUploadedFile("r.csv", data, content_type="text/csv")
        self.oc.post("/app/loads/import/", {"company":str(self.a.id),"file":f})
        ld = Load.objects.get(reference="T-900")
        self.assertEqual(ld.origin, "Sacramento CA")
        self.assertEqual(ld.destination, "Las Vegas NV")
        self.assertEqual(float(ld.rate), 1875.50)
        self.assertEqual(ld.stops.count("\n"), 2)

    def test_fuel_entry_with_receipt(self):
        v = Vehicle.objects.create(company=self.a, unit_number="A-1")
        self._set_company(self.oc, self.a)
        rf = SimpleUploadedFile("r.pdf", b"%PDF-1.4", content_type="application/pdf")
        self.oc.post("/app/fuel/add/", {"company":str(self.a.id),"date":"2026-08-10","vehicle":str(v.id),"location":"Pilot","gallons":"100","amount":"400","receipt":rf})
        self.assertTrue(FuelTransaction.objects.first().receipt)

    def test_expense_with_receipt(self):
        self._set_company(self.oc, self.a)
        ef = SimpleUploadedFile("e.pdf", b"%PDF-1.4", content_type="application/pdf")
        self.oc.post("/app/accounting/expense/add/", {"company":str(self.a.id),"date":"2026-08-10","category":"Repair","amount":"250","receipt":ef})
        self.assertTrue(Expense.objects.first().receipt)

    def test_owner_sees_all_companies(self):
        Load.objects.create(company=self.a, reference="AAA", origin="X", destination="Y", rate=1)
        Load.objects.create(company=self.b, reference="BBB", origin="P", destination="Q", rate=1)
        self._set_company(self.oc, None)
        loads = self.oc.get("/app/loads/").content.decode()
        self.assertIn("AAA", loads); self.assertIn("BBB", loads)

    def test_main_pages_load(self):
        self._set_company(self.oc, self.a)
        for url in ["/dashboard/","/app/loads/","/app/vehicles/","/app/fuel/","/app/accounting/","/app/pay/","/app/company/documents/"]:
            self.assertEqual(self.oc.get(url).status_code, 200, f"{url} failed")

    def test_hiring_pipeline_and_convert(self):
        ap = Applicant.objects.create(company=self.a, first_name="Ash", last_name="Pal",
            phone="555", cdl_number="D1", cdl_class="A", employment_history="x",
            signature="Ash Pal", consent=True)
        self._set_company(self.oc, self.a)
        # move stage records history
        self.oc.post(f"/app/hiring/{ap.id}/", {"action": "stage", "stage": "qualified", "reason": "ok"})
        ap.refresh_from_db()
        self.assertEqual(ap.stage, "qualified")
        self.assertEqual(ap.history.count(), 1)
        # convert to driver
        self.oc.post(f"/app/hiring/{ap.id}/", {"action": "convert"})
        ap.refresh_from_db()
        self.assertIsNotNone(ap.converted_driver)
        self.assertEqual(ap.stage, "active")

    def test_hiring_pipeline_isolation(self):
        other = Applicant.objects.create(company=self.b, first_name="Bob", last_name="Lee", phone="9")
        self.oc.post("/app/company/access/", {"company": str(self.a.id), "username": "wgh",
                                              "password": "secret12345", "role": "admin"})
        from django.contrib.auth.models import User as U
        wg = U.objects.get(username="wgh"); c = Client(); c.force_login(wg)
        board = c.get("/app/hiring/?all=1").content.decode()
        self.assertNotIn("Bob", board)
        r = c.get(f"/app/hiring/{other.id}/", follow=True)
        self.assertNotIn("Lee", r.content.decode())

    # ---- DOT inspection packet (driver's roadside screen) ----
    def _driver_client(self, company=None, **kw):
        """A driver with a login, ready to hit the /driver/ portal."""
        company = company or self.a
        d = Driver.objects.create(company=company, first_name="Raj", last_name="Gill",
                                  cdl_number="D9911", **kw)
        u = User.objects.create_user("raj", password="pw12345678")
        d.user = u; d.save()
        c = Client(); c.force_login(u)
        return d, c

    def test_dot_packet_statuses_and_default_truck(self):
        from operations.models import ComplianceDocument
        t = datetime.date.today()
        d, c = self._driver_client(medical_expiry=t - datetime.timedelta(days=5))
        v_old = Vehicle.objects.create(company=self.a, unit_number="OLD-1")
        v_new = Vehicle.objects.create(company=self.a, unit_number="NEW-2", plate="8XYZ123")
        Load.objects.create(company=self.a, driver=d, vehicle=v_old, reference="L-OLD",
                            origin="X", destination="Y", pickup_date=t - datetime.timedelta(days=20))
        Load.objects.create(company=self.a, driver=d, vehicle=v_new, reference="L-NEW",
                            origin="P", destination="Q", pickup_date=t - datetime.timedelta(days=2))
        ComplianceDocument.objects.create(company=self.a, driver=d, doc_type="cdl",
            expiry_date=t + datetime.timedelta(days=400),
            file=SimpleUploadedFile("cdl.pdf", b"%PDF-1.4"))
        ComplianceDocument.objects.create(company=self.a, driver=d, doc_type="mvr",
            expiry_date=t + datetime.timedelta(days=10),
            file=SimpleUploadedFile("mvr.pdf", b"%PDF-1.4"))
        VehicleDocument.objects.create(company=self.a, vehicle=v_new, doc_type="inspection",
            expiry_date=t - datetime.timedelta(days=3),
            file=SimpleUploadedFile("insp.pdf", b"%PDF-1.4"))
        CompanyDocument.objects.create(company=self.a, doc_type="coi",
            expiry_date=t + datetime.timedelta(days=200),
            file=SimpleUploadedFile("coi.pdf", b"%PDF-1.4"))

        r = c.get("/driver/dot-packet/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn("On file", html)          # CDL + COI
        self.assertIn("Expiring soon", html)    # MVR, 10 days out
        self.assertIn("Expired", html)          # medical card + truck inspection
        self.assertIn("Not on file", html)      # e.g. BOC-3, title
        # defaults to the truck on the most recent load, offers the other as an option
        self.assertIn("NEW-2", html)
        self.assertIn("OLD-1", html)
        self.assertIn('value="{}" selected'.format(v_new.id), html)

    def test_dot_packet_green_needs_an_actual_file(self):
        """A document row with no upload must not read as 'On file' — there's
        nothing for the officer to look at."""
        from operations.models import ComplianceDocument
        t = datetime.date.today()
        d, c = self._driver_client()
        ComplianceDocument.objects.create(company=self.a, driver=d, doc_type="mvr",
                                          expiry_date=t + datetime.timedelta(days=100))
        html = c.get("/driver/dot-packet/").content.decode()
        self.assertNotIn("On file", html)
        self.assertIn("Not on file", html)
        self.assertNotIn(">View<", html)

    def test_dot_packet_truck_switch_is_limited_to_own_trucks(self):
        t = datetime.date.today()
        d, c = self._driver_client()
        mine = Vehicle.objects.create(company=self.a, unit_number="MINE-1")
        theirs = Vehicle.objects.create(company=self.a, unit_number="THEIRS-9")
        Load.objects.create(company=self.a, driver=d, vehicle=mine, reference="L1",
                            origin="X", destination="Y", pickup_date=t)
        VehicleDocument.objects.create(company=self.a, vehicle=theirs, doc_type="title",
            title="SECRET-TITLE", file=SimpleUploadedFile("t.pdf", b"%PDF-1.4"))
        html = c.get(f"/driver/dot-packet/?vehicle={theirs.id}").content.decode()
        self.assertIn("MINE-1", html)           # falls back to their own truck
        self.assertNotIn("THEIRS-9", html)

    def test_dot_packet_no_loads_no_crash(self):
        d, c = self._driver_client()
        r = c.get("/driver/dot-packet/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("No truck on file yet", r.content.decode())

    def test_dot_packet_requires_a_driver_login(self):
        self._set_company(self.oc, self.a)
        r = self.oc.get("/driver/dot-packet/")
        self.assertEqual(r.status_code, 302)    # office user gets bounced to dashboard

    def test_dot_packet_link_on_driver_home_and_nav(self):
        d, c = self._driver_client()
        html = c.get("/driver/").content.decode()
        self.assertIn("/driver/dot-packet/", html)
        self.assertIn("DOT Packet", html)       # bottom nav from driver_base

    # ---- Billing alerts (dashboard money-in nags) ----
    def _delivered(self, company, ref, days_ago, **kw):
        """A delivered load whose delivered_at stamp is `days_ago` days old."""
        ld = Load.objects.create(company=company, reference=ref, origin="X", destination="Y",
                                 rate=1500, status="delivered", **kw)
        ld.delivered_at = timezone.now() - datetime.timedelta(days=days_ago)
        Load.objects.filter(pk=ld.pk).update(delivered_at=ld.delivered_at)
        return ld

    def _invoiced(self, company, ref, days_ago, **kw):
        """An invoiced load whose billed_at stamp is `days_ago` days old."""
        ld = Load.objects.create(company=company, reference=ref, origin="X", destination="Y",
                                 rate=1500, status="invoiced", **kw)
        ld.billed_at = timezone.now() - datetime.timedelta(days=days_ago)
        Load.objects.filter(pk=ld.pk).update(billed_at=ld.billed_at)
        return ld

    def test_load_stamps_delivered_at_and_billed_at_once(self):
        ld = Load.objects.create(company=self.a, reference="S1", origin="X", destination="Y")
        self.assertIsNone(ld.delivered_at)
        ld.status = "delivered"; ld.save()
        first = ld.delivered_at
        self.assertIsNotNone(first)
        self.assertIsNone(ld.billed_at)
        # bouncing back and forth must not re-stamp
        ld.status = "in_transit"; ld.save()
        ld.status = "delivered"; ld.save()
        self.assertEqual(ld.delivered_at, first)
        ld.status = "invoiced"; ld.save()
        self.assertIsNotNone(ld.billed_at)
        self.assertEqual(ld.delivered_at, first)

    def test_stamp_survives_a_narrow_update_fields_save(self):
        """The driver app marks delivery with save(update_fields=["status"]) —
        the stamp must not be silently dropped."""
        ld = Load.objects.create(company=self.a, reference="S2", origin="X", destination="Y")
        ld.status = "delivered"
        ld.save(update_fields=["status"])
        ld.refresh_from_db()
        self.assertIsNotNone(ld.delivered_at)

    def test_delivered_unbilled_load_is_ready_to_bill(self):
        from operations.views import _billing_alerts
        ld = self._delivered(self.a, "RB1", 1)
        out = _billing_alerts([self.a])
        self.assertEqual([r["load"].id for r in out["ready"]], [ld.id])
        self.assertEqual(out["awaiting"], [])

    def test_invoiced_unpaid_load_is_awaiting_payment(self):
        from operations.views import _billing_alerts
        ld = self._invoiced(self.a, "AP1", 1)
        out = _billing_alerts([self.a])
        self.assertEqual([r["load"].id for r in out["awaiting"]], [ld.id])
        self.assertEqual(out["ready"], [])

    def test_paid_load_appears_in_neither_list(self):
        from operations.views import _billing_alerts
        Load.objects.create(company=self.a, reference="P1", origin="X", destination="Y",
                            status="paid", payment_status="closed")
        out = _billing_alerts([self.a])
        self.assertEqual(out["ready"], [])
        self.assertEqual(out["awaiting"], [])

    def test_ready_to_bill_severity_thresholds(self):
        from operations.views import _billing_alerts
        self._delivered(self.a, "D0", 0)
        self._delivered(self.a, "D2", 2)
        self._delivered(self.a, "D5", 5)
        by_ref = {r["reference"]: r for r in _billing_alerts([self.a])["ready"]}
        self.assertEqual(by_ref["D0"]["severity"], "ok")
        self.assertEqual(by_ref["D2"]["severity"], "warn")     # warn at 2+
        self.assertEqual(by_ref["D5"]["severity"], "urgent")   # urgent at 5+

    def test_awaiting_payment_thresholds_follow_how_the_company_gets_paid(self):
        from operations.views import _billing_alerts
        self.a.factor = "RTS"; self.a.save()        # factored: 3 / 7
        self.b.factor = "None"; self.b.save()       # direct billed: 30 / 45
        self._invoiced(self.a, "F3", 3)
        self._invoiced(self.a, "F7", 7)
        self._invoiced(self.b, "N3", 3)
        self._invoiced(self.b, "N30", 30)
        self._invoiced(self.b, "N45", 45)
        by_ref = {r["reference"]: r for r in _billing_alerts([self.a, self.b])["awaiting"]}
        self.assertEqual(by_ref["F3"]["severity"], "warn")
        self.assertEqual(by_ref["F7"]["severity"], "urgent")
        self.assertEqual(by_ref["N3"]["severity"], "ok")       # still well inside net-30
        self.assertEqual(by_ref["N30"]["severity"], "warn")
        self.assertEqual(by_ref["N45"]["severity"], "urgent")

    def test_billing_alerts_sorted_oldest_first(self):
        from operations.views import _billing_alerts
        self._delivered(self.a, "NEW", 1)
        self._delivered(self.a, "OLD", 9)
        self._delivered(self.a, "MID", 4)
        self.assertEqual([r["reference"] for r in _billing_alerts([self.a])["ready"]],
                         ["OLD", "MID", "NEW"])

    def test_billing_alerts_are_scoped_to_the_given_companies(self):
        from operations.views import _billing_alerts
        mine = self._delivered(self.a, "MINE", 3)
        self._delivered(self.b, "THEIRS", 3)
        self._invoiced(self.b, "THEIRS-INV", 3)
        out = _billing_alerts([self.a])
        self.assertEqual([r["reference"] for r in out["ready"]], ["MINE"])
        self.assertEqual(out["awaiting"], [])
        self.assertEqual(mine.company_id, self.a.id)

    def test_dashboard_shows_billing_banners_only_for_own_companies(self):
        self._delivered(self.a, "BANNER-MINE", 3)
        self._invoiced(self.b, "BANNER-THEIRS", 3)
        self.oc.post("/app/company/access/", {"company": str(self.a.id), "username": "bd",
                                              "password": "secret12345", "role": "admin"})
        u = User.objects.get(username="bd"); c = Client(); c.force_login(u)
        html = c.get("/dashboard/").content.decode()
        self.assertIn("Ready to bill", html)
        self.assertIn("BANNER-MINE", html)
        self.assertNotIn("BANNER-THEIRS", html)

    def test_invoiced_but_already_settled_does_not_nag(self):
        """Money landed (factor released reserve / closed) but nobody advanced
        status to "paid" — must not sit in Awaiting payment forever."""
        from operations.views import _billing_alerts
        self._invoiced(self.a, "STILL-OWED", 4, payment_status="submitted")
        self._invoiced(self.a, "RESERVE-OUT", 4, payment_status="reserve_released")
        self._invoiced(self.a, "SETTLED", 4, payment_status="closed")
        refs = [r["reference"] for r in _billing_alerts([self.a])["awaiting"]]
        self.assertEqual(refs, ["STILL-OWED"])

    # ---- Maintenance: fuel cross-check + time-based fallback ----
    def _fuel(self, company, vehicle, gallons, days_ago, n=1):
        for i in range(n):
            FuelTransaction.objects.create(
                company=company, vehicle=vehicle, gallons=gallons,
                amount=float(gallons) * 4,
                date=datetime.date.today() - datetime.timedelta(days=days_ago + i))

    def _load_miles(self, company, vehicle, miles, days_ago, ref="M"):
        Load.objects.create(company=company, vehicle=vehicle, reference=ref,
                            origin="X", destination="Y", miles=miles,
                            pickup_date=datetime.date.today() - datetime.timedelta(days=days_ago))

    def test_mpg_comes_from_this_trucks_own_load_miles_and_gallons(self):
        from operations.views import _vehicle_mpg
        v = Vehicle.objects.create(company=self.a, unit_number="MPG-1")
        self._fuel(self.a, v, 50, 30, n=4)              # 200 gal
        self._load_miles(self.a, v, 1200, 20, ref="A")  # 1200 mi
        self._load_miles(self.a, v, 400, 25, ref="B")   # +400 = 1600 mi
        self.assertEqual(_vehicle_mpg(v), 8.0)          # 1600 / 200

    def test_mpg_is_none_without_enough_history(self):
        from operations.views import _vehicle_mpg
        v = Vehicle.objects.create(company=self.a, unit_number="MPG-2")
        self._fuel(self.a, v, 50, 10, n=2)              # only 2 fill-ups
        self._load_miles(self.a, v, 800, 10)
        self.assertIsNone(_vehicle_mpg(v))
        thin = Vehicle.objects.create(company=self.a, unit_number="MPG-3")
        self.assertIsNone(_vehicle_mpg(thin))           # no data at all

    def test_mpg_rejects_implausible_numbers(self):
        """Loads missing their miles, or fuel booked to the wrong truck, must not
        produce a bogus MPG that the estimate then nags on."""
        from operations.views import _vehicle_mpg
        v = Vehicle.objects.create(company=self.a, unit_number="MPG-4")
        self._fuel(self.a, v, 100, 30, n=4)             # 400 gal
        self._load_miles(self.a, v, 20000, 20)          # 50 mpg - impossible
        self.assertIsNone(_vehicle_mpg(v))

    def _thirsty_truck(self, company, unit, odometer):
        """A truck whose fuel burn implies ~4000 mi since service (500 gal x 8 mpg),
        on a 5000 mi interval from 10000 mi, i.e. estimated 1000 mi from service."""
        v = Vehicle.objects.create(
            company=company, unit_number=unit, status="active",
            service_interval_miles=5000, last_service_miles=10000,
            last_service_date=datetime.date.today() - datetime.timedelta(days=60),
            odometer=odometer)
        self._fuel(company, v, 125, 50, n=4)            # 500 gal since service
        self._load_miles(company, v, 4000, 40)          # 4000 mi / 500 gal = 8 mpg
        return v

    def test_fuel_estimate_fires_when_odometer_is_stale(self):
        from operations.views import _fuel_mileage_alerts
        v = self._thirsty_truck(self.a, "STALE-1", odometer=10050)  # barely moved
        out = _fuel_mileage_alerts([self.a])
        self.assertEqual([a["unit"] for a in out], ["STALE-1"])
        self.assertEqual(out[0]["mpg"], 8.0)
        self.assertAlmostEqual(out[0]["est_miles"], 4000, delta=5)
        self.assertEqual(out[0]["odometer"], 10050)
        self.assertEqual(v.miles_to_service, 4950)      # odometer says "plenty left"

    def test_fuel_estimate_stays_quiet_when_odometer_is_current(self):
        """If the odometer already shows the truck is near service, the hard
        mileage alert owns it — no duplicate 'verify mileage' nag."""
        from operations.views import _fuel_mileage_alerts, _maintenance_alerts
        self._thirsty_truck(self.a, "CURRENT-1", odometer=14000)   # 1000 mi to service
        self.assertEqual(_fuel_mileage_alerts([self.a]), [])
        self.assertEqual([a["unit"] for a in _maintenance_alerts([self.a])], ["CURRENT-1"])

    def test_fuel_estimate_stays_quiet_below_the_threshold(self):
        from operations.views import _fuel_mileage_alerts
        v = Vehicle.objects.create(company=self.a, unit_number="FRESH-1", status="active",
            service_interval_miles=25000, last_service_miles=10000, odometer=10050,
            last_service_date=datetime.date.today() - datetime.timedelta(days=10))
        self._fuel(self.a, v, 125, 5, n=4)              # 500 gal -> ~4000 mi est
        self._load_miles(self.a, v, 4000, 5)            # of a 25000 mi interval
        self.assertEqual(_fuel_mileage_alerts([self.a]), [])

    def test_fuel_estimate_skips_trucks_with_thin_fuel_history(self):
        from operations.views import _fuel_mileage_alerts
        v = Vehicle.objects.create(company=self.a, unit_number="THIN-1", status="active",
            service_interval_miles=5000, last_service_miles=10000, odometer=10050,
            last_service_date=datetime.date.today() - datetime.timedelta(days=60))
        self._fuel(self.a, v, 200, 50, n=2)             # only 2 fill-ups -> no MPG
        self._load_miles(self.a, v, 4000, 40)
        self.assertEqual(_fuel_mileage_alerts([self.a]), [])

    def test_fuel_estimate_is_scoped_to_the_given_companies(self):
        from operations.views import _fuel_mileage_alerts
        self._thirsty_truck(self.a, "MINE-F", odometer=10050)
        self._thirsty_truck(self.b, "THEIRS-F", odometer=10050)
        self.assertEqual([a["unit"] for a in _fuel_mileage_alerts([self.a])], ["MINE-F"])
        self.assertEqual([a["unit"] for a in _fuel_mileage_alerts([self.b])], ["THEIRS-F"])

    def test_time_based_service_alert_fires_at_25_days(self):
        from operations.views import _service_time_alerts
        today = datetime.date.today()
        Vehicle.objects.create(company=self.a, unit_number="IDLE-25", status="active",
                               last_service_date=today - datetime.timedelta(days=25))
        Vehicle.objects.create(company=self.a, unit_number="IDLE-40", status="active",
                               last_service_date=today - datetime.timedelta(days=40))
        Vehicle.objects.create(company=self.a, unit_number="FRESH-24", status="active",
                               last_service_date=today - datetime.timedelta(days=24))
        Vehicle.objects.create(company=self.a, unit_number="UNKNOWN", status="active")
        out = _service_time_alerts([self.a])
        self.assertEqual([a["unit"] for a in out], ["IDLE-40", "IDLE-25"])  # oldest first
        self.assertEqual(out[1]["days"], 25)

    def test_time_based_service_alert_is_scoped_to_the_given_companies(self):
        from operations.views import _service_time_alerts
        old = datetime.date.today() - datetime.timedelta(days=40)
        Vehicle.objects.create(company=self.a, unit_number="MINE-T", status="active",
                               last_service_date=old)
        Vehicle.objects.create(company=self.b, unit_number="THEIRS-T", status="active",
                               last_service_date=old)
        self.assertEqual([a["unit"] for a in _service_time_alerts([self.a])], ["MINE-T"])

    def test_logging_a_scheduled_service_resets_the_clock_but_a_repair_does_not(self):
        from operations.models import MaintenanceRecord
        today = datetime.date.today()
        v = Vehicle.objects.create(company=self.a, unit_number="SVC-1", status="active",
                                   odometer=90000)
        MaintenanceRecord.objects.create(company=self.a, vehicle=v, date=today,
                                         part="Oil change + filter", odometer=90000)
        v.refresh_from_db()
        self.assertEqual(v.last_service_date, today)
        self.assertEqual(v.last_service_miles, 90000)
        # a repair must not make the truck look freshly serviced
        MaintenanceRecord.objects.create(company=self.a, vehicle=v,
                                         date=today + datetime.timedelta(days=5),
                                         part="Tire replacement", odometer=92000)
        v.refresh_from_db()
        self.assertEqual(v.last_service_date, today)
        self.assertEqual(v.last_service_miles, 90000)
        # and back-dating an older service must not rewind the clock
        MaintenanceRecord.objects.create(company=self.a, vehicle=v,
                                         date=today - datetime.timedelta(days=30),
                                         part="Lube service", odometer=80000)
        v.refresh_from_db()
        self.assertEqual(v.last_service_date, today)
        self.assertEqual(v.last_service_miles, 90000)

    def test_dashboard_renders_the_two_new_checks_separately(self):
        today = datetime.date.today()
        self._thirsty_truck(self.a, "VERIFY-ME", odometer=10050)
        Vehicle.objects.create(company=self.a, unit_number="IDLE-ME", status="active",
                               last_service_date=today - datetime.timedelta(days=33))
        self._set_company(self.oc, self.a)
        html = self.oc.get("/dashboard/").content.decode()
        self.assertIn("Verify mileage", html)
        self.assertIn("VERIFY-ME", html)
        self.assertIn("Service check due", html)
        self.assertIn("IDLE-ME", html)
        self.assertIn("33 days", html)

    # ---- Editing mileage / service settings from the vehicle page ----
    def test_office_can_turn_on_mileage_alerts_from_the_vehicle_page(self):
        """The three fields the mileage alerts need must be settable from the
        dashboard, not only the Django admin."""
        from operations.views import _maintenance_alerts
        v = Vehicle.objects.create(company=self.a, unit_number="EDIT-1", status="active")
        self._set_company(self.oc, self.a)
        self.assertIsNone(v.miles_to_service)
        self.assertEqual(_maintenance_alerts([self.a]), [])
        self.oc.post(f"/app/vehicles/{v.id}/mileage/", {
            "odometer": "116,500", "service_interval_miles": "17000",
            "last_service_miles": "100000", "last_service_date": "2026-09-01"})
        v.refresh_from_db()
        self.assertEqual(v.odometer, 116500)            # commas tolerated
        self.assertEqual(v.service_interval_miles, 17000)
        self.assertEqual(v.last_service_miles, 100000)
        self.assertEqual(v.last_service_date, datetime.date(2026, 9, 1))
        self.assertEqual(v.miles_to_service, 500)       # now computable
        self.assertEqual([a["unit"] for a in _maintenance_alerts([self.a])], ["EDIT-1"])

    def test_mileage_form_leaves_blank_fields_alone(self):
        v = Vehicle.objects.create(company=self.a, unit_number="EDIT-2", status="active",
                                   odometer=500000, service_interval_miles=17000,
                                   last_service_miles=495000)
        self._set_company(self.oc, self.a)
        self.oc.post(f"/app/vehicles/{v.id}/mileage/", {"odometer": "505000",
                     "service_interval_miles": "", "last_service_miles": ""})
        v.refresh_from_db()
        self.assertEqual(v.odometer, 505000)
        self.assertEqual(v.service_interval_miles, 17000)   # untouched
        self.assertEqual(v.last_service_miles, 495000)      # untouched

    def test_mileage_form_rejects_a_backwards_odometer(self):
        """A typo that winds mileage back would make an overdue truck look fresh."""
        v = Vehicle.objects.create(company=self.a, unit_number="EDIT-3", status="active",
                                   odometer=500000)
        self._set_company(self.oc, self.a)
        self.oc.post(f"/app/vehicles/{v.id}/mileage/", {"odometer": "50000"})
        v.refresh_from_db()
        self.assertEqual(v.odometer, 500000)

    def test_mileage_form_rejects_last_service_above_the_odometer(self):
        v = Vehicle.objects.create(company=self.a, unit_number="EDIT-4", status="active")
        self._set_company(self.oc, self.a)
        self.oc.post(f"/app/vehicles/{v.id}/mileage/",
                     {"odometer": "100000", "last_service_miles": "200000"})
        v.refresh_from_db()
        self.assertEqual(v.odometer, 100000)
        self.assertIsNone(v.last_service_miles)

    def test_mileage_form_is_company_scoped(self):
        other = Vehicle.objects.create(company=self.b, unit_number="OTHER-1", status="active")
        self.oc.post("/app/company/access/", {"company": str(self.a.id), "username": "mw",
                                              "password": "secret12345", "role": "admin"})
        u = User.objects.get(username="mw"); c = Client(); c.force_login(u)
        c.post(f"/app/vehicles/{other.id}/mileage/", {"odometer": "999999"})
        other.refresh_from_db()
        self.assertIsNone(other.odometer)   # untouched across the tenant boundary

    def test_logging_a_service_carries_the_odometer_onto_the_truck(self):
        """The shop reads the dash, so a service record's reading updates the
        truck - but only forwards, so rental 'period miles' can't wind it back."""
        from operations.models import MaintenanceRecord
        today = datetime.date.today()
        v = Vehicle.objects.create(company=self.a, unit_number="ODO-1", status="active",
                                   service_interval_miles=17000)
        MaintenanceRecord.objects.create(company=self.a, vehicle=v, date=today,
                                         part="Oil Change", odometer=840514)
        v.refresh_from_db()
        self.assertEqual(v.odometer, 840514)
        self.assertEqual(v.last_service_miles, 840514)
        # a rental record whose "odometer" is really miles-driven must not rewind it
        MaintenanceRecord.objects.create(company=self.a, vehicle=v,
                                         date=today + datetime.timedelta(days=1),
                                         part="Paid miles 13900", odometer=13900)
        v.refresh_from_db()
        self.assertEqual(v.odometer, 840514)
        # a later repair with a genuine higher reading does move it
        MaintenanceRecord.objects.create(company=self.a, vehicle=v,
                                         date=today + datetime.timedelta(days=2),
                                         part="Caliper installed / labor", odometer=845000)
        v.refresh_from_db()
        self.assertEqual(v.odometer, 845000)
        self.assertEqual(v.last_service_miles, 840514)   # repair didn't reset the clock

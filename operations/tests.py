"""
Automated test suite — checks the whole system's core features.
Run it anytime with:   python manage.py test operations
Each test is one safety check. Green = working, Red = something broke.
"""
import datetime, tempfile
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
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

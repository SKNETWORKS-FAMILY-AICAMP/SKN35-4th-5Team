"""Deployment checks must fail closed without leaking database credentials."""
import io
import os
import runpy
from pathlib import Path
from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import OperationalError
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse


class DatabaseReadinessTests(TestCase):
    def test_ready_after_migrations_without_calling_ai(self):
        with mock.patch("core.ai_client.health") as ai_health:
            response = self.client.get(reverse("core:ready"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok", "migrations": "ok"})
        ai_health.assert_not_called()
        output = io.StringIO()
        call_command("check_database", stdout=output)
        self.assertIn("Migrations: OK", output.getvalue())

    def test_pending_migrations_block_readiness(self):
        with mock.patch("core.views.pending_migration_count", return_value=3):
            self.assertEqual(self.client.get(reverse("core:ready")).status_code, 503)
        with mock.patch("core.management.commands.check_database.pending_migration_count", return_value=3):
            with self.assertRaises(CommandError):
                call_command("check_database", stdout=io.StringIO())
            call_command("check_database", allow_unmigrated=True, stdout=io.StringIO())

    def test_database_failure_is_redacted(self):
        failure = OperationalError("postgresql://user:secret-value@private-db/db")
        with mock.patch("core.views.pending_migration_count", side_effect=failure):
            response = self.client.get(reverse("core:ready"))
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("secret-value", response.content.decode())
        with mock.patch("core.management.commands.check_database.pending_migration_count", side_effect=failure):
            with self.assertRaises(CommandError) as caught:
                call_command("check_database")
        self.assertNotIn("secret-value", str(caught.exception))

    @override_settings(SECURE_SSL_REDIRECT=True, SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True)
    def test_health_is_available_on_loopback_while_login_requires_https(self):
        self.assertEqual(self.client.get(reverse("core:ready")).status_code, 200)
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.url.startswith("https://"))
        response = self.client.get(reverse("accounts:login"), HTTP_X_FORWARDED_PROTO="https")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cookies["csrftoken"]["secure"])


class ProductionConfigurationTests(SimpleTestCase):
    def load_config(self, **updates):
        values = {
            "DJANGO_DEBUG": "False",
            "DJANGO_SECRET_KEY": "test-only-configuration-key-" * 3,
            "DATABASE_URL": "mysql://app:test@db.example.test:3306/beaurette",
            "DJANGO_ALLOWED_HOSTS": "beaurette.example.test",
        }
        values.update(updates)
        path = Path(__file__).resolve().parents[1] / "config" / "settings.py"
        with mock.patch.dict(os.environ, values, clear=True), mock.patch("dotenv.load_dotenv"):
            return runpy.run_path(str(path))

    def test_production_requires_database_and_strong_secret(self):
        for updates in ({"DATABASE_URL": ""}, {"DATABASE_URL": "sqlite:///:memory:"}, {"DJANGO_SECRET_KEY": "short"}):
            with self.subTest(updates=updates), self.assertRaises(ImproperlyConfigured):
                self.load_config(**updates)

    def test_production_verifies_rds_endpoint_even_if_url_disables_tls(self):
        config = self.load_config(DATABASE_URL="postgresql://app:test@db.example.test:5432/beaurette?sslmode=disable")
        db = config["DATABASES"]["default"]
        self.assertEqual(db["OPTIONS"]["sslmode"], "verify-full")
        self.assertEqual(db["OPTIONS"]["sslrootcert"], "/app/certs/rds-global-bundle.pem")
        self.assertEqual(db["OPTIONS"]["connect_timeout"], 5)
        self.assertIn("beaurette.example.test", config["ALLOWED_HOSTS"])
        self.assertIn("127.0.0.1", config["ALLOWED_HOSTS"])

    def test_local_development_still_defaults_to_sqlite(self):
        config = self.load_config(DJANGO_DEBUG="True", DATABASE_URL="", DJANGO_SECRET_KEY="")
        self.assertEqual(config["DATABASES"]["default"]["ENGINE"], "django.db.backends.sqlite3")

    def test_mysql_production_requires_verified_tls_and_strict_unicode_storage(self):
        config = self.load_config(
            DATABASE_URL="mysql://app:test@db.example.test:3306/beaurette?ssl_mode=DISABLED&charset=latin1",
            DATABASE_SSL_ROOT_CERT="/certs/custom-ca.pem",
        )
        db = config["DATABASES"]["default"]
        self.assertEqual(db["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(db["OPTIONS"]["ssl_mode"], "VERIFY_IDENTITY")
        self.assertEqual(db["OPTIONS"]["ssl"], {"ca": "/certs/custom-ca.pem"})
        self.assertEqual(db["OPTIONS"]["connect_timeout"], 5)
        self.assertEqual(db["OPTIONS"]["charset"], "utf8mb4")
        self.assertEqual(db["OPTIONS"]["isolation_level"], "read committed")
        self.assertIn("STRICT_TRANS_TABLES", db["OPTIONS"]["init_command"])

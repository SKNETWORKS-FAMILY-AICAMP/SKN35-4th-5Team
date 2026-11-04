from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError
from django.db.migrations.exceptions import InconsistentMigrationHistory

from core.database import pending_migration_count


class Command(BaseCommand):
    help = "Check DB connectivity and migrations without changing data or printing credentials."

    def add_arguments(self, parser):
        parser.add_argument("--allow-unmigrated", action="store_true", help="For the first connection check, before migrate.")

    def handle(self, *args, **options):
        try:
            pending = pending_migration_count()
        except (DatabaseError, InconsistentMigrationHistory) as error:
            raise CommandError(f"Database check failed ({type(error).__name__}). Check RDS access, credentials and TLS.") from None
        self.stdout.write("Database connection: OK")
        if pending:
            self.stdout.write(f"Migrations pending: {pending}")
            if not options["allow_unmigrated"]:
                raise CommandError("Run manage.py migrate before starting the web service.")
        else:
            self.stdout.write(self.style.SUCCESS("Migrations: OK"))

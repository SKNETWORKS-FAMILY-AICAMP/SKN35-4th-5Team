"""Read-only database readiness checks; never include connection secrets in errors."""
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


def pending_migration_count() -> int:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    executor = MigrationExecutor(connection)
    return len(executor.migration_plan(executor.loader.graph.leaf_nodes()))

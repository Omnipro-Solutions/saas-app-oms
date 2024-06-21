from enum import Enum

from celery import current_task, shared_task
from django.conf import settings
from django.db import connection, connections, transaction
from django.utils import timezone
from omni_pro_oms.models import Operation, Task


class DeleteTasks:
    @staticmethod
    @shared_task(
        max_retries=settings.CELERY_MAX_RETRIES,
        default_retry_delay=settings.CELERY_SECONDS_TIME_TO_RETRY,
        queue=settings.CELERY_NAME_QUEUE,
    )
    def task_delete_tasks():
        try:
            return DeleteTasks().task_info()
        except Exception as exc:
            print(f"Tarea fallida: {exc}")
            raise current_task.retry(exc=exc, countdown=settings.CELERY_SECONDS_TIME_TO_RETRY)

    @transaction.atomic
    def task_info(self):
        operations = Operation.objects.filter(
            success_clean_task_days__isnull=False,
            other_clean_task_days__isnull=False,
            packages_to_clean_count__isnull=False,
        )
        for operation in operations:
            success_tasks_oms = self._fetch_tasks("omni_pro_oms_task", "success", operation.success_clean_task_days)
            success_tasks_celery = self._fetch_tasks(
                "django_celery_results_taskresult",
                "SUCCESS",
                operation.success_clean_task_days,
                date_field="date_created",
            )
            other_tasks_oms = self._fetch_tasks(
                "omni_pro_oms_task", ["error", "waiting", "partial_success"], operation.other_clean_task_days
            )
            other_tasks_celery = self._fetch_tasks(
                "django_celery_results_taskresult",
                ["FAILURE", "PENDING", "RETRY"],
                operation.other_clean_task_days,
                date_field="date_created",
            )
            limit = operation.packages_to_clean_count
            (
                limited_success_tasks_oms,
                limited_other_tasks_oms,
                limited_success_tasks_celery,
                limited_other_tasks_celery,
            ) = self._package_task(
                operation, success_tasks_oms, success_tasks_celery, other_tasks_oms, other_tasks_celery, limit
            )
        return self.delete_task(
            limited_success_tasks_oms,
            limited_other_tasks_oms,
            limited_success_tasks_celery,
            limited_other_tasks_celery,
        )

    def _fetch_tasks(self, table_name, status, days_to_keep, date_field="created_at"):
        cutoff_date = timezone.now() - timezone.timedelta(days=days_to_keep)
        status_condition = f"status = '{status}'" if isinstance(status, str) else f"status IN {tuple(status)}"

        query = f"""
            SELECT *
            FROM {table_name}
            WHERE {status_condition}
            AND {date_field} <= %s
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [cutoff_date])
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching tasks from {table_name}: {e}")
            return []

    def _package_task(
        self, operation, success_tasks_oms, success_tasks_celery, other_tasks_oms, other_tasks_celery, limit_delete
    ):
        try:
            with connection.cursor() as cursor:
                limited_success_tasks_oms = self._apply_limit(
                    cursor, "omni_pro_oms_task", success_tasks_oms, limit_delete
                )
                limited_other_tasks_oms = self._apply_limit(cursor, "omni_pro_oms_task", other_tasks_oms, limit_delete)
                limited_success_tasks_celery = self._apply_limit(
                    cursor, "django_celery_results_taskresult", success_tasks_celery, limit_delete
                )
                limited_other_tasks_celery = self._apply_limit(
                    cursor, "django_celery_results_taskresult", other_tasks_celery, limit_delete
                )

            return (
                limited_success_tasks_oms,
                limited_other_tasks_oms,
                limited_success_tasks_celery,
                limited_other_tasks_celery,
            )
        except Exception as e:
            print(f"Error packaging tasks: {e}")
            return [], [], [], []

    def _apply_limit(self, cursor, table_name, tasks, limit):
        task_ids = tuple(task[0] for task in tasks)
        if not task_ids:
            return []

        if table_name == "omni_pro_oms_task":
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE id IN %s
                ORDER BY created_at ASC
                LIMIT %s
            """

        else:
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE id IN %s
                ORDER BY date_created ASC
                LIMIT %s
            """

        cursor.execute(query, [task_ids, limit])
        return cursor.fetchall()

    def delete_task(
        self,
        limited_success_tasks_oms,
        limited_other_tasks_oms,
        limited_success_tasks_celery,
        limited_other_tasks_celery,
    ):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    self._delete_tasks(cursor, "omni_pro_oms_task", limited_success_tasks_oms)
                    self._delete_tasks(cursor, "omni_pro_oms_task", limited_other_tasks_oms)
                    self._delete_tasks(cursor, "django_celery_results_taskresult", limited_success_tasks_celery)
                    self._delete_tasks(cursor, "django_celery_results_taskresult", limited_other_tasks_celery)
                transaction.set_rollback(False)
                print("Transaction committed successfully.")
        except Exception as e:
            print(f"Error deleting tasks: {e}")

    def _delete_tasks(self, cursor, table_name, tasks):
        task_ids = tuple(task[0] for task in tasks)
        if not task_ids:
            print(f"No tasks to delete in {table_name}")
            return

        query = f"""
            DELETE FROM {table_name}
            WHERE id IN %s
        """

        try:
            print(f"Executing delete query: {query} with task_ids: {task_ids}")
            cursor.execute(query, [task_ids])
            print(f"Deleted tasks with IDs {task_ids} from {table_name}")
        except Exception as e:
            print(f"Error executing delete query for {table_name}: {e}")

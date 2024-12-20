import json

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django_celery_results.admin import TaskResultAdmin
from django_celery_results.models import TaskResult
from omni_pro_base.admin import BaseAdmin

admin.site.unregister(TaskResult)


class CustomTaskResultAdmin(TaskResultAdmin):
    list_display = [
        "task_id",
        "periodic_task_name",
        "task_name",
        "date_done",
        "status",
        "worker",
        "oms_task",
    ]

    def oms_task(self, obj):
        try:
            if obj.task_args:
                print(f"task_args crudo: {repr(obj.task_args)}")
                task_args = obj.task_args.strip('"')

                task_args = task_args.replace("(", "").replace(")", "").replace(",", "").strip()
                task_args = "".join(task_args.split())

                if task_args.isdigit():
                    url = reverse("admin:omni_pro_oms_task_change", args=[int(task_args)])
                    return format_html('<a href="{}" target="_blank">Ver Task</a>', url)

            return "No disponible"
        except Exception as e:
            return format_html(f"<span style='color: red;'>Error: {e}</span>")

    oms_task.short_description = "OMS Task"


admin.site.register(TaskResult, CustomTaskResultAdmin)

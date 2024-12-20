import django
from django.contrib import admin
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from omni_pro_base.admin import BaseAdmin
from omni_pro_oms.forms import TaskAdminForm
from omni_pro_oms.models import Task
from rangefilter.filters import DateRangeFilter
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        fields = (
            "id",
            "item",
            "created_at",
            "tenant_id",
            "operation_id",
            "tenant_operation_id",
            "status",
            "url_src",
            "url_dst",
            "time",
            "updated_at",
            "celery_task_id",
        )
        export_order = fields


class BuilderDateRangeFilter(DateRangeFilter):
    def get_form(self, _request):
        form_class = self._get_form_class()
        if django.VERSION[:2] >= (5, 0):
            for name, value in self.used_parameters.items():
                if isinstance(value, list):
                    self.used_parameters[name] = value[-1]
        return form_class(self.used_parameters or None)


class TaskAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = TaskResource

    list_display = (
        "id",
        "celery_task_id",
        "item",
        "created_at",
        "tenant_id",
        "operation_id",
        "tenant_operation_id",
        "status",
        "url_src",
        "url_dst",
        "time",
        "updated_at",
    )
    list_filter = (
        "tenant_id",
        "operation_id",
        "status",
        ("created_at", BuilderDateRangeFilter),
        "updated_at",
    )
    search_fields = ("item", "url_src", "url_dst", "body_src", "body_dst", "time")
    form = TaskAdminForm

    def __init__(self, *args, **kwargs):
        super(TaskAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = (
            (
                _("Required Information"),
                {"fields": ("name", "tenant_id", "operation_id", "status", "time", "item", "celery_task_id")},
            ),
            (
                _("Source Info"),
                {
                    "fields": (
                        "body_src",
                        "headers_src",
                        "params_src",
                        "response_src",
                        "url_src",
                    )
                },
            ),
            (
                _("Destination Info"),
                {
                    "fields": (
                        "body_dst",
                        "headers_dst",
                        "params_dst",
                        "response_dst",
                        "url_dst",
                    )
                },
            ),
        ) + self.fieldsets

    def retry_task(self, request, queryset):
        try:
            for task in queryset:
                if task.status != "error":
                    continue
                task_view = resolve(task.url_src)
                view = task_view.func.view_class()
                factory = APIRequestFactory()

                # Crea la solicitud con el diccionario JSON y el método HTTP especificado
                method = task.operation_id.http_method.lower()
                request_rest = getattr(factory, method)(task.url_src, task.body_src, content_type="application/json")

                # Convertimos HttpRequest a una instancia de Request
                request_rest = Request(request_rest, parsers=[view.parser_classes[0]])
                request_rest._full_data = task.body_src

                # Llamamos al método dinámico de la vista
                view_method = getattr(view, method)
                view_method(request=request_rest, **task_view.kwargs)
                return self.message_user(request, "Task retried successfully.")
        except Exception as e:
            print(str(e))
            self.message_user(request, f"Error: {str(e)}", 40)

    actions = [retry_task]


admin.site.register(Task, TaskAdmin)

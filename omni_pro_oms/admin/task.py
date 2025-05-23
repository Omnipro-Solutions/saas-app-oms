import django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from omni_pro_base.admin import BaseAdmin
from omni_pro_oms.forms import TaskAdminForm
from omni_pro_oms.models import Task
from rangefilter.filters import DateRangeFilter
from omni_pro_oms.utils import retry_task_single

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
                retry_task_single(task)
                return self.message_user(request, "Task retried successfully.")
        except Exception as e:
            print(str(e))
            self.message_user(request, f"Error: {str(e)}", 40)

    actions = [retry_task]

    def save_model(self, request, obj, form, change):
        """
        Overrides the save_model method to set a custom attribute before saving the model.
        Args:
            request (HttpRequest): The current request object.
            obj (Model): The model instance being saved.
            form (ModelForm): The form instance used to create or update the model.
            change (bool): A flag indicating whether the model is being changed (True) or added (False).
        """

        if change:
            obj._admin_panel = True
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)

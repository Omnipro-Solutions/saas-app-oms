from django.apps import AppConfig


class OmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "omni_pro_oms"

    def ready(self):
        import omni_pro_oms.models.signals

        return super().ready()

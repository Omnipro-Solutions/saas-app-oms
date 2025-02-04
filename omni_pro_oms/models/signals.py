from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from omni_pro_oms.models import Task


@receiver(pre_save, sender=Task)
def set_old_status(sender, instance, **kwargs):
    """
    Signal handler to set the old status of a Task instance before it is saved.
    This function is intended to be connected to the pre-save signal of the Task model.
    It checks if the instance being saved already exists in the database (i.e., it has a primary key).
    If it does, it retrieves the current status of the instance from the database and stores it in the
    instance's _old_status attribute. If the instance is new (i.e., it does not have a primary key yet),
    it sets the _old_status attribute to None.
    Args:
        sender (Model): The model class that sent the signal.
        instance (Model instance): The instance of the model that is being saved.
        **kwargs: Additional keyword arguments.
    """

    if instance.pk:
        old = Task.objects.filter(pk=instance.pk).values("status").first()
        if old:
            instance._old_status = old["status"]  # Save the previous status
        else:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def send_email_on_error_status(sender, instance, created, **kwargs):
    """
    Sends an email notification when the status of an instance changes to a specific value.
    This function is intended to be used as a Django signal handler for the post_save signal.
    It sends an email notification only when the instance is updated (not created) and the status
    changes to a specific value defined in the related operation_id.
    Args:
        sender (Model): The model class that sent the signal.
        instance (Model instance): The actual instance being saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    Conditions for sending an email:
        - The instance is not newly created.
        - The old status is different from the new status.
        - The new status matches the status_notifications of the related operation_id.
        - The related operation_id has active notifications.
        - The related operation_id has specified email addresses.
        - The update is not performed from the admin panel.
    Email content:
        - Subject: Status change notification with the task name and ID.
        - Message: Details about the task and its new status.
        - Recipients: Email addresses specified in the related operation_id.
    """

    # We avoid emails during creation, only for updates
    if not created:
        old_status = getattr(instance, "_old_status", None)
        new_status = instance.status
        admin_panel = getattr(instance, "_admin_panel", False)

        if (
            old_status != instance.operation_id.status_notifications
            and new_status == instance.operation_id.status_notifications
            and instance.operation_id.active_notifications
            and instance.operation_id.emails
            and not admin_panel
        ):
            status: str = instance.operation_id.status_notifications
            asunto = f"{status.capitalize()} en tarea {instance.name} con ID {instance.pk}"
            mensaje = f"La tarea {instance.name} con ID {instance.pk} ha pasado a estado de {status}."
            destinatarios = instance.operation_id.emails

            send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, destinatarios, fail_silently=False)

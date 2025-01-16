from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_json_widget.widgets import JSONEditorWidget
from omni_pro_oms.models import Operation


class OperationAdminForm(forms.ModelForm):
    emails = SimpleArrayField(forms.EmailField(), required=False, widget=forms.Textarea(attrs={"rows": 4, "cols": 20}))

    class Meta:
        model = Operation
        fields = "__all__"
        widgets = {
            "headers": JSONEditorWidget,
        }

    def clean_emails(self):
        emails = self.cleaned_data.get("emails", [])
        # Validate if emails are unique
        if len(emails) != len(set(emails)):
            raise forms.ValidationError("Duplicate emails are not allowed.")
        return emails

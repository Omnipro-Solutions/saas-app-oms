from django import forms
from django_json_widget.widgets import JSONEditorWidget
from omni_pro_oms.models import Config


class ConfigAdminForm(forms.ModelForm):

    token = forms.CharField(
        label="Token",
        required=False,
        widget=forms.Textarea(attrs={"disabled": "disabled"}),
    )
    expires_in = forms.IntegerField(
        label="Time to token expiration",
        required=False,
        widget=forms.NumberInput(attrs={"disabled": "disabled"}),
    )
    expires_at = forms.DateTimeField(
        label="Date To token expiration",
        required=False,
        widget=forms.DateTimeInput(attrs={"disabled": "disabled"}),
    )

    class Meta:
        model = Config
        fields = "__all__"
        widgets = {"auth": JSONEditorWidget}

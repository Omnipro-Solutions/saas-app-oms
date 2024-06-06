from django import forms
from omni_pro_oms.models import Tenant


class TenantAdminForm(forms.ModelForm):
    minutes_remaining = forms.CharField(
        label="Minutes Remaining", required=False, widget=forms.TextInput(attrs={"disabled": "disabled"})
    )

    class Meta:
        model = Tenant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["minutes_remaining"].initial = self.instance.minutes_remaining

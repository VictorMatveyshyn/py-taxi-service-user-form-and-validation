from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) == 8:
            if license_number[:3].isalpha() and license_number[:3].isupper():
                if license_number[3:].isdigit():
                    return license_number
        raise ValidationError(
            "Incorrect license format. "
            "Must contain 3 uppercase letters and 5 digits."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) == 8:
            if license_number[:3].isalpha() and license_number[:3].isupper():
                if license_number[3:].isdigit():
                    return license_number
        raise ValidationError(
            "Incorrect license format. "
            "Must contain 3 uppercase letters and 5 digits."
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"

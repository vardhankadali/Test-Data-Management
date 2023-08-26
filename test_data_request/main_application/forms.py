from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password']


class SupplierForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Supplier
        fields = CustomUserForm.Meta.fields


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class RequesterForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(RequesterForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Requester
        fields = CustomUserForm.Meta.fields


class ManagerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Manager
        fields = CustomUserForm.Meta.fields


class SupplierEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(SupplierEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Supplier
        fields = CustomUserForm.Meta.fields 


class RequesterEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(RequesterEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Requester
        fields = CustomUserForm.Meta.fields


class ManagerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ManagerEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Manager
        fields = CustomUserForm.Meta.fields


class RaiseRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RaiseRequestForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'] = forms.ChoiceField(
            choices=[(o.first_name + " " + o.last_name, o.first_name + " " + o.last_name) for o in CustomUser.objects.filter(user_type=3)]
        )
    class Meta():
        model = Request
        fields = ["status", "assigned_to", "type_of_request", "env_swimlane",
               "project_name", "number_of_records", "application", "expected_date", "type_of_data_setup",
               "stakeholders", "state_jurisdiction", "synopsis_of_request", "description_of_request"]

class UpdateRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateRequestForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'] = forms.ChoiceField(
            choices=[(o.first_name + " " + o.last_name, o.first_name + " " + o.last_name) for o in CustomUser.objects.filter(user_type=3)]
        )
    class Meta():
        model = Request
        fields = ["status", "assigned_to","test_data"]
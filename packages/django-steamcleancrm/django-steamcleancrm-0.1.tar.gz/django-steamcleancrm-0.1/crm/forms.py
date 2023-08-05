from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.db.models import fields
from .models import Lead, WorkOrder, WorkOrderImages, WorkOrderTechnicians

# Create your forms here.


class CreateLeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        exclude = ('is_active',)


class UpdateLeadForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = Lead
        fields = '__all__'


class CreateWorkOrderForm(forms.ModelForm):
    estimate_date = forms.DateField(widget=AdminDateWidget)
    estimate_time = forms.TimeField(widget=AdminTimeWidget)
    appointment_date = forms.DateField(widget=AdminDateWidget, required=False)
    appointment_time = forms.TimeField(widget=AdminTimeWidget, required=False)

    class Meta:
        model = WorkOrder
        fields = ('job_description', 'estimate_date', 'estimate_time', 'appointment_date', 'appointment_time')


class UpdateWorkOrderForm(forms.ModelForm):
    estimate_date = forms.DateField(widget=AdminDateWidget)
    estimate_time = forms.TimeField(widget=AdminTimeWidget)
    appointment_date = forms.DateField(widget=AdminDateWidget)
    appointment_time = forms.TimeField(widget=AdminTimeWidget)
    is_complete = forms.BooleanField(required=False)
    is_canceled = forms.BooleanField(required=False)

    class Meta:
        model = WorkOrder
        fields = ('job_description', 'estimate_date', 'estimate_time', 'appointment_date', 'appointment_time', 'is_complete', 'is_canceled')


class CloseWorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('is_complete', 'is_canceled' )


class SubmitWorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('is_complete', 'is_canceled')


class AddTechnicianToWorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrderTechnicians
        fields = ('technician', )


class AddImageToWorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrderImages
        fields = ('image', )

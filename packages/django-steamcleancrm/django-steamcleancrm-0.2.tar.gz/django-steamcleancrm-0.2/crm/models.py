from django.db import models
from . import utilities
from django.contrib.auth.models import User

# Models start here


# Keeps track of customers and their contact information
class Lead(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    email = models.EmailField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/lead/%i/" % self.id


# A work order can only be opened wirh a Lead instance passed as an argument   
class WorkOrder(models.Model):
    lead = models.ForeignKey(Lead, default=None, on_delete=models.CASCADE)
    job_description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    estimate_date = models.DateField(blank=True, null=True)
    estimate_time = models.TimeField(blank=True, null=True)
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return "Work Order #%i" % self.id

    def get_absolute_url(self):
        return "/lead/%i/work-order/%i/" % (self.lead.id, self.id)


# The models below hold information pertaining to specific work order instances
class WorkOrderTechnicians(models.Model):
    work_order = models.ForeignKey(WorkOrder, default=None, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, default=None, on_delete=models.CASCADE)


class WorkOrderImages(models.Model):
    work_order = models.ForeignKey(WorkOrder, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=utilities.get_image_filename, verbose_name='Image')


# class WorkOrderSurvey(models.Model):
#     work_order = models.ForeignKey(WorkOrder, default=None, on_delete=models.CASCADE)

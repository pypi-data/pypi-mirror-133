from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Lead)
admin.site.register(models.WorkOrder)
admin.site.register(models.WorkOrderImages)
admin.site.register(models.WorkOrderTechnicians)
# admin.site.register(models.WorkOrderSurvey)


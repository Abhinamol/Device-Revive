from django.contrib import admin


# Register your models here.

from . import models
# Register your models here

admin.site.register(models.Userdetails)
admin.site.register(models.Booking)
admin.site.register(models.SecondHandProduct)
admin.site.register(models.Payment)
admin.site.register(models.Order)
admin.site.register(models.Technician)


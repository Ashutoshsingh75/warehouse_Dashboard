from django.contrib import admin
from .models import LaundryUser,Laundrytype,Laundry,LaundryshopeUser,Order_details
# Register your models here.
admin.site.register(LaundryUser)
admin.site.register(Laundrytype)
admin.site.register(Laundry)
admin.site.register(LaundryshopeUser)
admin.site.register(Order_details)

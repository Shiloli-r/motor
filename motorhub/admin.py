from django.contrib import admin
from .models import Manufacturers, Cars, Customers, Orders, Contact, Notifications, Cart


# Register your models here.
admin.site.register(Manufacturers)
admin.site.register(Cars)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(Contact)
admin.site.register(Notifications)
admin.site.register(Cart)

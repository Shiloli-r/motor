from django.contrib import admin
from .models import Cars
from .models import Customers
from .models import Orders

# Register your models here.
admin.site.register(Cars)
admin.site.register(Customers)
admin.site.register(Orders)
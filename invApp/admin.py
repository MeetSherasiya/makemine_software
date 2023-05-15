from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Tempitem)
admin.site.register(CustomerBill)
admin.site.register(invoiceitem)
admin.site.register(stockhistory)
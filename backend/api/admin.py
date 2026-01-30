from django.contrib import admin
from .models import FinancialRecord, GSTRecord, BankStatement

admin.site.register(FinancialRecord)
admin.site.register(GSTRecord)
admin.site.register(BankStatement)

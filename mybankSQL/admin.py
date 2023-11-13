from django.contrib import admin
from mybankSQL.models import Account, Deposit, Withdrawal, Transfer, TransactionID, AccountID, Demo

# Register your models here.

admin.site.register(Account)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Transfer)
admin.site.register(TransactionID)
admin.site.register(AccountID)
admin.site.register(Demo)

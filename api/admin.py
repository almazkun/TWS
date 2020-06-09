from django.contrib import admin
from .models import LoanProgram, LoanBorrower, LoanInquiry, Untrusted

# Register your models here.
admin.site.register(LoanProgram)
admin.site.register(LoanBorrower)
admin.site.register(LoanInquiry)
admin.site.register(Untrusted)

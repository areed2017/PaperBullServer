from django.contrib import admin

from api.models import *


class StockModel(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'sector', 'industry', 'dividend_yield', 'short_percent_of_float', 'outstanding_shares')


admin.site.register(Stock, StockModel)
admin.site.register(Portfolio)
admin.site.register(Short)
admin.site.register(StockPrice)

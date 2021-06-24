from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    free_cash = models.DecimalField(max_digits=20, decimal_places=5, default=1000.00)


class Stock(models.Model):
    ticker = models.CharField(max_length=6)
    sector = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    short_percent_of_float = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    outstanding_shares = models.IntegerField(null=True)
    last_update = models.DateTimeField(default=now)


class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shares = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    buy_price = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=4, null=True)


class Short(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    volume = models.IntegerField()


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.IntegerField()

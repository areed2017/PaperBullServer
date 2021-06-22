from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    ticker = models.TextField()
    sector = models.TextField()
    industry = models.TextField()
    dividend_yield = models.DecimalField()
    short_percent_of_float = models.DecimalField()
    outstanding_shares = models.IntegerField()


class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_price = models.DecimalField()
    sell_price = models.DecimalField()


class Short(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    volume = models.IntegerField()


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    open = models.DecimalField()
    high = models.DecimalField()
    low = models.DecimalField()
    close = models.DecimalField()
    volume = models.IntegerField()

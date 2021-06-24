from datetime import timedelta, datetime, date

import pytz
import requests
import yfinance as yf
from django.contrib.auth.models import User
from api.models import Stock, StockPrice, Short


def authenticate(func):
    def authenticate_and_call(*args, **kwargs):
        return func(*args, **kwargs)
    return authenticate_and_call


def get_user(request):
    return User.objects.all()[0]


def get_stock(ticker: str):
    stock, created = Stock.objects.get_or_create(ticker=ticker)
    today = datetime.now().replace(tzinfo=pytz.UTC)
    if created:
        stock.last_update = today - timedelta(days=10)
    if stock.last_update.day == today.day and stock.last_update.month == today.month:
        return stock

    data = yf.Ticker(ticker)
    stock.sector = data.info.get('sector', None)
    stock.industry = data.info.get('industry', None)
    stock.dividend_yield = data.info.get('dividendYield', 0.0)
    stock.short_percent_of_float = data.info.get('shortPercentOfFloat', 0.0)
    stock.outstanding_shares = data.info.get('sharesOutstanding', 0.0)

    stock.save()
    return stock


def update_stock_intraday(stock: Stock):
    today = datetime.now().replace(tzinfo=pytz.UTC)
    end_date = datetime.today()
    start_date = end_date - timedelta(7)

    if StockPrice.objects.filter(stock=stock).count() > 0:
        last = StockPrice.objects.filter(stock=stock).order_by('id')[0]
        if stock.last_update.day == today.day and stock.last_update.month == today.month:
            return stock
        if last.date_time > start_date.replace(tzinfo=pytz.UTC):
            start_date = last.date_time

    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    data = yf.download(stock.ticker, start_date, end_date, interval='1m')

    for date, row in data.iterrows():
        if StockPrice.objects.filter(stock=stock, date_time=date).count() > 0:
            continue
        stock_price = StockPrice(
            stock=stock,
            date_time=date,
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Adj Close'],
            volume=row['Volume']
        )
        stock_price.save()

    stock.last_update = today
    stock.save()


def update_shorts():
    index = datetime(2018, 8, 1, tzinfo=pytz.UTC)
    if Short.objects.all().count() > 0:
        last = Short.objects.all().order_by('-date')[0]
        index = last.date
    end = datetime.now().replace(tzinfo=pytz.UTC)
    day = timedelta(days=1)

    print("Updating Shorts")
    stocks = {}
    while index <= end:
        if index.weekday() >= 5 or Short.objects.filter(date=index):
            index = index + day
            continue
        print(index)
        url = f'http://regsho.finra.org/CNMSshvol{index.strftime("%Y%m%d")}.txt'
        data = requests.get(url)

        save_list = []
        for line in data.text.split('\n'):
            if "ShortVolume" in line:
                continue
            line_data = line.replace(',',':').split("|")
            if len(line_data) < 2:
                continue
            if line_data[1] not in stocks:
                stocks[line_data[1]] = get_stock(line_data[1])
            save_list += [Short(stock=stocks[line_data[1]], date=index, volume=int(line_data[2]))]
        Short.objects.bulk_create(save_list)

        index = index + day

    print("Shorts updated.")

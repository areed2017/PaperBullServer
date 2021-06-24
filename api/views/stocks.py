from threading import Thread

from django.http import JsonResponse

from api.models import Short, Portfolio, UserData
from api.views.__util__ import *


@authenticate
def get_ticker_intra_day(request, ticker):
    stock = get_stock(ticker)
    Thread(target=lambda s=stock: update_stock_intraday(s)).start()

    latest_data = StockPrice.objects.filter(stock=stock)
    data = []
    for price in latest_data:
        data += [{
            'date_time': price.date_time,
            'open': price.open,
            'high': price.high,
            'low': price.low,
            'close': price.close,
            'volume': price.volume
        }]

    return JsonResponse({'data': data})


@authenticate
def get_ticker_short_data(request, ticker):
    stock = get_stock(ticker)
    Thread(target=update_shorts).start()

    short_data = Short.objects.filter(stock=stock)
    data = []
    for short in short_data:
        data += [{
            'date': short.date,
            'volume': short.volume
        }]

    return JsonResponse({'data': data})


@authenticate
def get_current_share_price(request, ticker):
    stock = get_stock(ticker)
    Thread(target=lambda s=stock: update_stock_intraday(s)).start()
    if StockPrice.objects.filter(stock=stock).count() > 0:
        data = StockPrice.objects.filter(stock=stock).order_by('-id')[0]
        return JsonResponse({'price': data.close})
    return JsonResponse({'price': 0.0})


@authenticate
def buy_share(request, ticker):
    user = get_user(request)
    stock = get_stock(ticker)
    user_data = UserData.objects.filter(user=user)[0]
    update_stock_intraday(stock)
    last_price = StockPrice.objects.filter(stock=stock).order_by('-id')[0].close
    if user_data.free_cash >= last_price:
        portfolio, _ = Portfolio.objects.get_or_create(user=user, stock=stock)
        user_data.free_cash -= last_price
        portfolio.shares += 1
        if portfolio.shares == 1:
            portfolio.buy_price = last_price
        else:
            # Warning: Not the real average
            portfolio.buy_price = (portfolio.buy_price + last_price) / 2
        portfolio.save()
        user_data.save()
        return JsonResponse({'success': False})

    else:
        return JsonResponse({'success': False})


def sell_share(request, ticker):
    user = get_user(request)
    stock = get_stock(ticker)
    user_data = UserData.objects.filter(user=user)[0]
    update_stock_intraday(stock)
    last_price = StockPrice.objects.filter(stock=stock).order_by('-id')[0].close

    portfolio, _ = Portfolio.objects.get_or_create(user=user, stock=stock)
    user_data.free_cash += last_price * portfolio.shares
    portfolio.shares = 0
    portfolio.sell_price = last_price

    user_data.save()
    portfolio.save()

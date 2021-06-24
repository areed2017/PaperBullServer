from django.http import JsonResponse

from api.models import UserData, Portfolio
from api.views.__util__ import *


@authenticate
def free_cash(request):
    user = get_user(request)
    user_data, _ = UserData.objects.get_or_create(user=user)
    user_data.save()
    return JsonResponse({
        'value': round(user_data.free_cash, 2)
    })


@authenticate
def get_portfolio(request):
    user = get_user(request)
    portfolio = Portfolio.objects.filter(user=user)
    data = []
    for share in portfolio:
        data += [{
            'stock': share.stock.ticker,
            'shares': share.shares,
            'buy_price': share.buy_price,
            'sell_price': share.sell_price,
        }]
    return JsonResponse({'data': data})


@authenticate
def get_portfolio_value(request):
    user = get_user(request)
    portfolio = Portfolio.objects.filter(user=user)
    user_data, _ = UserData.objects.get_or_create(user=user)
    user_data.save()
    cash = user_data.free_cash
    for share in portfolio:
        last_price = StockPrice.objects.filter(stock=share.stock).order_by('-id')[0].close
        cash += last_price * share.shares

    return JsonResponse({'value': cash})


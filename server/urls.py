"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/free_cash', free_cash),
    path('account/portfolio', get_portfolio),
    path('account/portfolio_value', get_portfolio_value),
    path('<str:ticker>/intra_day', get_ticker_intra_day),
    path('<str:ticker>/shorts', get_ticker_short_data),
    path('<str:ticker>/price', get_current_share_price),
    path('<str:ticker>/buy_share', buy_share),
    path('<str:ticker>/sell_share', sell_share),
]
